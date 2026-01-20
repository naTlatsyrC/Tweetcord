"""
Migration script to add text_filter column to existing notification table.
Run this script once to update your existing database.
"""
import os
import asyncio
import aiosqlite
from src.log import setup_logger

log = setup_logger(__name__)

async def migrate_database():
    """Add text_filter column to notification table if it doesn't exist."""
    db_path = os.path.join(os.getenv('DATA_PATH'), 'tracked_accounts.db')
    
    if not os.path.exists(db_path):
        log.info("Database file does not exist. No migration needed.")
        return
    
    async with aiosqlite.connect(db_path) as db:
        # Check if text_filter column already exists
        async with db.execute("PRAGMA table_info(notification)") as cursor:
            columns = await cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            if 'text_filter' in column_names:
                log.info("text_filter column already exists. No migration needed.")
                return
        
        # Add the text_filter column
        try:
            await db.execute("ALTER TABLE notification ADD COLUMN text_filter TEXT DEFAULT NULL")
            await db.commit()
            log.info("Successfully added text_filter column to notification table.")
        except Exception as e:
            log.error(f"Error adding text_filter column: {e}")
            raise

if __name__ == "__main__":
    # Set up DATA_PATH if not already set
    if not os.getenv('DATA_PATH'):
        os.environ['DATA_PATH'] = './data'
    
    asyncio.run(migrate_database())
    print("Migration completed successfully!")
