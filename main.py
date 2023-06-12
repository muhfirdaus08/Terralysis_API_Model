from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, declarative_base

from typing import List, Dict, Union
import os
import uvicorn
import uuid
import random
import string

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow import keras
from keras.preprocessing import image
import io
import numpy as np
from PIL import Image
from google.cloud import storage

app = FastAPI()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, func
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

# Memuat variabel lingkungan dari file .env
load_dotenv()
Base = declarative_base()

# Konfigurasi koneksi database Local MySQL
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")

# Membuat URL koneksi database
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Membuat engine dan session database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Menguji koneksi ke database
try:
    engine.connect()
    print("Berhasil terhubung ke database")
except:
    print("Gagal terhubung ke database")

Base = declarative_base()


class ImageTable(Base):
    __tablename__ = "images"

    imageId = Column(String, primary_key=True, default=str(uuid.uuid4()))
    userId = Column(String, nullable=False)
    url = Column(String, nullable=False)
    originalname = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    kelas = Column(String, nullable=False)
    short_desc = Column(String, nullable=False)
    long_desc = Column(String, nullable=False)
    kandungan = Column(String, nullable=False)
    persebaran = Column(String, nullable=False)
    ciri_fisik = Column(String, nullable=False)
    ciri_kimia = Column(String, nullable=False)
    ciri_morfologi = Column(String, nullable=False)
    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(
        DateTime, default=func.now(), onupdate=datetime.utcnow, nullable=False
    )


class ImageTableGuest(Base):
    __tablename__ = "imagesGuests"

    imageGuestId = Column(String, primary_key=True, default=str(uuid.uuid4()))
    url = Column(String, nullable=False)
    originalname = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    kelas = Column(String, nullable=False)
    short_desc = Column(String, nullable=False)
    long_desc = Column(String, nullable=False)
    kandungan = Column(String, nullable=False)
    persebaran = Column(String, nullable=False)
    ciri_fisik = Column(String, nullable=False)
    ciri_kimia = Column(String, nullable=False)
    ciri_morfologi = Column(String, nullable=False)
    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(
        DateTime, default=func.now(), onupdate=datetime.utcnow, nullable=False
    )


model = keras.models.load_model("./model_2.h5")


async def prediksi(gambar):
    # Load the image
    labels = ["Alluvial", "Black", "Clay", "Red"]
    img = Image.open(gambar)
    img = img.resize((260, 260))
    x = np.array(img)
    x = np.expand_dims(x, axis=0)

    # Normalization
    x = x / 255.0

    # Predicting the image
    proba = model.predict(x)[0]
    maxx = proba.max()

    # Displaying the best prediction result
    max_index = np.argmax(proba)
    best_label = labels[max_index]
    best_proba = proba[max_index] * 100

    if best_proba >= 0.5:
        return "{}: {:.2f}%".format(best_label, best_proba)
    else:
        return "\nMaaf, tanah ini tidak terdeteksi!"


def getLabel(string):
    index = string.find(":")
    if index != -1:
        first_word = string[:index].strip()
        return first_word
    else:
        return None


def getShortDesc(label):
    descriptions = {
        "Alluvial": "Tanah Hasil Endapan",
        "Black": "Tanah Humus atau Organik",
        "Clay": "Tanah yang Lentur (tanah liat)",
        "Red": "Tanah Laterit",
    }
    return descriptions.get(label, "Deskripsi tidak tersedia")


def getLongDesc(label):
    descriptions = {
        "Alluvial": "Tanah Alluvial adalah jenis tanah yang terbentuk oleh endapan sedimen yang dibawa oleh aliran sungai dan terdeposit di dataran banjir atau lembah sungai. Tanah ini biasanya kaya akan bahan organik dan nutrisi yang baik untuk pertumbuhan tanaman",
        "Black": "Tanah Hitam, juga dikenal sebagai tanah Chernozem, adalah jenis tanah yang sangat subur dengan horison atas yang kaya akan bahan organik. Tanah ini cenderung memiliki warna hitam atau gelap akibat kandungan tinggi bahan organik.",
        "Clay": "Tanah Liat adalah jenis tanah dengan kandungan partikel lempung yang tinggi. Partikel lempung yang halus memberikan tekstur yang lengket dan kepadatan yang tinggi. Tanah Liat cenderung memiliki kemampuan retensi air yang baik, tetapi juga dapat menjadi keras ketika kering.",
        "Red": "Tanah Merah adalah jenis tanah yang memiliki warna merah atau kemerahan akibat kandungan tinggi zat besi oksida. Tanah ini sering ditemukan di daerah tropis dan subtropis. Tanah Merah dapat memiliki kandungan nutrisi yang terbatas dan pH yang rendah.",
    }
    return descriptions.get(label, "Deskripsi tidak tersedia")


def getKandungan(label):
    descriptions = {
        "Alluvial": "Kandungan bahan organik tinggi. Nutrisi yang baik, seperti nitrogen, fosfor, dan kalium. Mineral yang berasal dari sedimen sungai, seperti lempung, pasir, dan kerikil.",
        "Black": "Kandungan bahan organik tinggi. Nutrisi yang baik, seperti nitrogen, fosfor, dan kalium. Mineral yang berasal dari sedimen sungai, seperti lempung, pasir, dan kerikil.",
        "Clay": "Kandungan partikel lempung yang tinggi. Retensi air yang baik. Kapasitas pertukaran kation yang tinggi, yang berarti kemampuan tanah untuk menyimpan dan melepaskan nutrisi kepada tanaman. Kaya akan mineral dan unsur hara, tetapi membutuhkan manajemen drainase yang baik.",
        "Red": "Kandungan zat besi oksida, yang memberikan warna merah. Umumnya memiliki pH yang rendah hingga sedikit asam. Nutrisi yang terkait dengan batuan asalnya, seperti kandungan rendah fosfor dan kapur.",
    }
    return descriptions.get(label, "Kandungan tidak tersedia")


def getPersebaran(label):
    descriptions = {
        "Alluvial": "Tanah Alluvial umumnya ditemukan di dataran banjir atau lembah sungai di seluruh dunia. Contoh yang terkenal adalah delta sungai Nil di Mesir, delta sungai Mississippi di Amerika Serikat, delta sungai Ganges di India, dan lembah sungai Amazon di Amerika Selatan.",
        "Black": "Tanah Hitam biasanya ditemukan di daerah yang sebelumnya terdapat aktivitas vulkanik. Contoh yang terkenal adalah tanah hitam di Dataran Tinggi Dekkan di India, di sekitar Gunung Vesuvius di Italia, dan beberapa daerah vulkanik di Indonesia.",
        "Clay": "Tanah Liat dapat ditemukan di berbagai daerah di seluruh dunia, terutama di daerah yang memiliki curah hujan yang tinggi. Contoh wilayah dengan tanah liat yang signifikan adalah Midwest Amerika Serikat, Delta Sungai Mekong di Vietnam, dan beberapa wilayah di Inggris.",
        "Red": "Tanah Merah sering ditemukan di daerah tropis dan subtropis. Contoh yang terkenal adalah tanah merah di wilayah tropis Afrika seperti Kongo, tanah merah di wilayah utara Australia, dan tanah merah di beberapa bagian Amerika Selatan seperti Brasil.",
    }
    return descriptions.get(label, "Persebaran tidak tersedia")


def getCiri_fisik(label):
    descriptions = {
        "Alluvial": "Tanah Alluvial memiliki tekstur yang bervariasi, mulai dari pasir hingga lempung, tergantung pada komposisi sedimen sungai. Mereka umumnya memiliki struktur butir kasar dan kepadatan yang rendah.",
        "Black": "Tanah Hitam memiliki tekstur yang beragam, dari pasir hingga lempung berat, tetapi sering kali memiliki kandungan lempung yang tinggi. Mereka memiliki struktur butir yang agregat dan kemampuan drainase yang baik.",
        "Clay": "Tanah Liat memiliki kandungan partikel lempung yang tinggi, memberikan tekstur yang halus dan lengket. Mereka memiliki daya tahan air yang tinggi dan cenderung menjadi keras ketika kering.",
        "Red": "Tanah Merah sering kali memiliki tekstur yang beragam, mulai dari pasir hingga lempung, tetapi seringkali mengandung partikel lempung yang lebih rendah. Mereka memiliki struktur butir yang agregat dan drainase yang bervariasi tergantung pada kondisi fisik tanah.",
    }
    return descriptions.get(label, "Ciri fisik tidak tersedia")


def getCiri_kimia(label):
    descriptions = {
        "Alluvial": "Tanah Alluvial umumnya memiliki kandungan bahan organik yang tinggi, pH netral hingga sedikit asam, dan kandungan nutrisi yang baik karena adanya material organik yang terdeposisi oleh air.",
        "Black": "Tanah Hitam kaya akan bahan organik, mineral seperti magnesium dan besi, serta memiliki pH netral hingga sedikit basa. Mereka juga memiliki kapasitas penahanan air yang baik.",
        "Clay": "Tanah Liat memiliki kapasitas pertukaran kation yang tinggi, yang berarti mereka mampu menyimpan dan melepaskan nutrisi dengan baik. pH tanah liat bisa bervariasi, tetapi cenderung lebih asam.",
        "Red": "Tanah Merah memiliki kandungan zat besi oksida yang tinggi, memberikan warna merah khas. pH tanah merah bisa rendah hingga sedikit asam. Nutrisi tertentu seperti fosfor dapat terbatas dalam tanah merah.",
    }
    return descriptions.get(label, "Ciri kimia tidak tersedia")


def getCiri_morfologi(label):
    descriptions = {
        "Alluvial": "Tanah Alluvial sering memiliki horison atas yang lebih gelap dan kaya akan bahan organik, yang kemudian menurun seiring dengan kedalaman tanah.",
        "Black": "Tanah Hitam biasanya memiliki horison atas yang sangat gelap dan kaya akan bahan organik, yang memberikan warna hitam khas.",
        "Clay": "Tanah Liat sering kali memiliki struktur agregat yang padat dan horison atas yang kaya akan bahan organik.",
        "Red": "Tanah Merah sering kali memiliki horison atas yang merah terang, yang kemudian berubah menjadi horison yang lebih pucat atau abu-abu dengan kedalaman tanah. Struktur dan drainase tanah merah dapat bervariasi tergantung pada kondisi dan sejarah pembentukan tanah.",
    }
    return descriptions.get(label, "Ciri morfologi tidak tersedia")


# get objek session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_random_string(length):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return "".join(random.choices(letters, k=length))


async def changeName(filename, uploader):
    extension = os.path.splitext(filename)[1]
    random_digits = generate_random_string(12)
    new_filename = f"{uploader}-{random_digits}{extension}"
    return new_filename


# Fungsi untuk mengunggah gambar ke direktori
def simpan_gambar(file, file_path):
    with open(file_path, "wb") as f:
        f.write(file.read())


# Konfigurasi kredensial Google Cloud Storage
storage_client = storage.Client.from_service_account_json(
    "./terralysis-storage-upload-key.json"
)
bucket_name = "terralysis-storage"

# Make static folder
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def read_root():
    return {"Status": "OK"}


# Upload Image By UserId
@app.post("/analysis")
async def upload_image(
    file: UploadFile = File(...),
    userId: str = Query(..., description="User ID"),
    db: Session = Depends(get_db),
):
    # PREDIKSI GAMBAR
    prediction_result = await prediksi(file.file)
    label = getLabel(prediction_result)

    file.file.seek(0)  # Mengatur posisi baca kembali ke awal
    upload_dir = "user-images"
    os.makedirs(upload_dir, exist_ok=True)
    changedName = await changeName(file.filename, "user")
    # SIMPAN GAMBAR KE LOKAL
    # simpan_gambar(file.file, os.path.join(upload_dir, changedName))

    # SIMPAN GAMBAR KE CLOUD STORAGE
    image_data = await file.read()
    filename = f"user-images/{changedName}"
    blob = storage_client.bucket(bucket_name).blob(filename)
    blob.upload_from_string(image_data, content_type="image/jpeg")
    blob.make_public()
    url = blob.public_url

    image_id = str(uuid.uuid4())

    # SIMPAN DATA GAMBAR KE DATABASE
    image = ImageTable(
        imageId=image_id,
        userId=userId,
        url=url,
        originalname=file.filename,
        mimetype=file.content_type,
        size=file.file.seek(0, os.SEEK_END),
        kelas=prediction_result,
        short_desc=getShortDesc(label),
        long_desc=getLongDesc(label),
        kandungan=getKandungan(label),
        persebaran=getPersebaran(label),
        ciri_fisik=getCiri_fisik(label),
        ciri_kimia=getCiri_kimia(label),
        ciri_morfologi=getCiri_morfologi(label),
    )
    db.add(image)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={
            "message": "Image User Upload Successfully and Get Prediction",
            "imageId": image_id,
            "url": url,
            "kelas": prediction_result,
        },
    )


# Get All Image By UserId
def filter_image_data(image):
    return {
        "imageId": image.imageId,
        "url": image.url,
        "kelas": image.kelas,
        "createdAt": image.createdAt,
    }


@app.get("/analysis/{userId}", response_model=None)
async def get_user_images(
    userId: str, db: Session = Depends(get_db)
) -> List[ImageTable]:
    user_images = db.query(ImageTable).filter(ImageTable.userId == userId).all()
    if not user_images:
        # raise HTTPException(status_code=404, detail="User Has No Images")
        return {
            "status_code": 200,
            "message": "User Has No Images",
        }

    filtered_images = [filter_image_data(image) for image in user_images]

    return {
        "status_code": 200,
        "message": "Get All Images User Success",
        "image": filtered_images,
    }


# Get Image By UserId and ImageId
@app.get("/analysis/{userId}/{imageId}", response_model=None)
async def get_user_image(
    userId: str, imageId: str, db: Session = Depends(get_db)
) -> ImageTable:
    user_image = (
        db.query(ImageTable)
        .filter(ImageTable.userId == userId, ImageTable.imageId == imageId)
        .first()
    )
    if not user_image:
        # raise HTTPException(status_code=404, detail="Image Not Found")
        return {"status_code": 200, "message": "Image Not Found"}

    return {
        "status_code": 200,
        "message": "Get Detail Image User Success",
        "image": user_image,
    }


# Delete Image By UserId and ImageId
@app.delete("/analysis/{userId}/{imageId}")
async def delete_image(userId: str, imageId: str, db: Session = Depends(get_db)):
    image = (
        db.query(ImageTable)
        .filter(ImageTable.userId == userId, ImageTable.imageId == imageId)
        .first()
    )
    if not image:
        # raise HTTPException(status_code=404, detail="Image Not Found")
        return {"status_code": 200, "message": "Image Not Found"}

    db.delete(image)
    db.commit()

    # Menghapus file gambar dari direktori
    file_path = os.path.join("uploads", image.originalname)
    if os.path.exists(file_path):
        os.remove(file_path)

    return {"status_code": 200, "message": "Delete Image Success"}


# Upload Image By Guest
@app.post("/analysis-guest")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # PREDIKSI GAMBAR
    prediction_result = await prediksi(file.file)
    label = getLabel(prediction_result)

    file.file.seek(0)  # Mengatur posisi baca kembali ke awal
    upload_dir = "guest-images"
    os.makedirs(upload_dir, exist_ok=True)
    changedName = await changeName(file.filename, "guest")
    # SIMPAN GAMBAR KE LOKAL
    # simpan_gambar(file.file, os.path.join(upload_dir, changedName))

    # SIMPAN GAMBAR KE CLOUD STORAGE
    image_data = await file.read()
    filename = f"guest-images/{changedName}"
    blob = storage_client.bucket(bucket_name).blob(filename)
    blob.upload_from_string(image_data, content_type="image/jpeg")
    blob.make_public()
    url = blob.public_url

    image_id = str(uuid.uuid4())

    # SIMPAN DATA GAMBAR KE DATABASE
    image = ImageTableGuest(
        imageGuestId=image_id,
        url=url,
        originalname=file.filename,
        mimetype=file.content_type,
        size=file.file.seek(0, os.SEEK_END),
        kelas=prediction_result,
        short_desc=getShortDesc(label),
        long_desc=getLongDesc(label),
        kandungan=getKandungan(label),
        persebaran=getPersebaran(label),
        ciri_fisik=getCiri_fisik(label),
        ciri_kimia=getCiri_kimia(label),
        ciri_morfologi=getCiri_morfologi(label),
    )
    db.add(image)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={
            "message": "Image Guest Upload Successfully and Get Prediction",
            "imageGuestId": image_id,
            "url": url,
            "kelas": prediction_result,
        },
    )


# Get Detail Image Guest
@app.get("/analysis-guest/{image_guestId}", response_model=None)
async def get_user_image(
    image_guestId: str, db: Session = Depends(get_db)
) -> ImageTableGuest:
    guest_image = (
        db.query(ImageTableGuest)
        .filter(ImageTableGuest.imageGuestId == image_guestId)
        .first()
    )
    if not guest_image:
        # raise HTTPException(status_code=404, detail="Image Not Found")
        return {"status_code": 200, "message": "Image Not Found"}

    return {
        "status_code": 200,
        "message": "Get Detail Image Guest Success",
        "image": guest_image,
    }


# port = 8080

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=port)
