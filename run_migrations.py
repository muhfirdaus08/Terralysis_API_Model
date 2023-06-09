from main import Base, engine
from migrations import upgrade

# Membuat tabel menggunakan skrip migrasi
Base.metadata.create_all(bind=engine)
upgrade(engine)
