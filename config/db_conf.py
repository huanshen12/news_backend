from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True,
    pool_size = 10,
    max_overflow = 20,
                                   )

AsyncSessionLocal = async_sessionmaker(
    bind = async_engine,
    class_ = AsyncSession,
    expire_on_commit = False
)

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.close()

