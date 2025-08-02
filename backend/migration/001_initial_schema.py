async def up(db):
    print("Applying initial schema migration...")
    # Example: Create an index on the messages collection
    await db.messages.create_index("session_id")
    print("Migration 001 applied.")

async def down(db):
    print("Rolling back initial schema migration...")
    await db.messages.drop_index("session_id")
    print("Migration 001 rolled back.")
