import database
from models import Base
import logging
from schema import CreateUserSchema
from controllers import CreateUserController
from config import config
import asyncio
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Seed Database")

async def recreate_db(engine,Base):
    # Drop and recreate tables to ensure a clean slate
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def create_admin_user():
# Create an admin user based on the configuration settings
   admin_user=CreateUserSchema(username=config.admin_username,
                               email=config.admin_email,
                               plain_password=config.admin_password,
                               first_name=config.admin_first_name,
                               last_name=config.admin_last_name)
   # Create session and call the controller to create the admin user
   async with database.SessionLocal() as session:
        await CreateUserController(admin_user,session, is_admin=True)

async def main():
    logger.info("Recreating database... 🫕")
    # Recreate the database schema
    try:
      await recreate_db(database.engine, Base)
      logger.info("Database recreated successfully ... 🍜")
      logger.info("Creating admin user based on configuration... 🧑‍💻")
      await create_admin_user()
      logger.info("Admin user created successfully based on your configuration settings... 🪪")
      logger.info("Database seeding completed successfully, You can start using the application now... 🎉")
    except Exception as e:
      logger.error(f"An error occurred while seeding the database: {e}")


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
