# <div align="center">📚 BookBrain-Azure</div>

<div align="center">

[![Azure Functions](https://img.shields.io/badge/azure%20functions-%230062CC.svg?style=for-the-badge&logo=azure-functions&logoColor=white)](https://azure.microsoft.com/en-us/services/functions/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-%23412991.svg?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

*An advanced serverless platform that revolutionizes educational content processing and study analytics.*

**Developed by [Khaled Ben Abderrahim](https://github.com/KhaledBenAbderrahim)**

---

## 🚀 Key Features

<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20bookBrain%20features.png" width="80%" alt="BookBrain Features">

---

## 💻 Tech Stack

<div align="center">
<table>
<tr>
<td align="center">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/azure/azure-original.svg" width="40" height="40"/><br>
Azure Functions
</td>
<td align="center">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="40" height="40"/><br>
Python
</td>
<td align="center">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg" width="40" height="40"/><br>
PostgreSQL
</td>
<td align="center">
<img src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/openai.svg" width="40" height="40"/><br>
OpenAI
</td>
</tr>
</table>
</div>

---

## 🔧 Components

<table>
<tr>
<td width="50%">

### 1. PDF Chunking Function
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20pdf%20chunking%20function.png" width="100%">

</td>
<td width="50%">

### 2. Study Progress Function
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20Study%20progress%20function.png" width="100%">

</td>
</tr>
<tr>
<td width="50%">

### 3. Upload Book Function
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20upload%20book%20function.png" width="100%">

</td>
<td width="50%">

### 4. Hourly Study Digest
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20Hourly%20Study%20Digest.png" width="100%">

</td>
</tr>
</table>

---

## ⚙️ Setup & Configuration

<details>
<summary><b>📝 Installation Steps</b></summary>

1. Clone the repository
```bash
git clone https://github.com/KhaledBenAbderrahim/BookBrain-Azure.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment variables
   - Copy `.env.example` to `.env`
   - Fill in your Azure credentials and other settings

4. Start the Azure Functions host
```bash
func start
```
</details>

<details>
<summary><b>🔑 Environment Variables</b></summary>

Required environment variables (see `.env.example`):
- `AZURE_STORAGE_CONNECTION_STRING`: Azure Storage connection string
- `DB_HOST`: Database host
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
</details>

---

## 🎯 Target Users

<div align="center">

| 📚 Educational Institutions | 💻 E-Learning Platforms | 👨‍🎓 Students and Educators |
|:-------------------------:|:----------------------:|:-------------------------:|
| 📖 Content Publishers | 🏫 Learning Management Systems | 📱 Educational Apps |

</div>

---

## 📚 API Documentation

API documentation is available via Swagger UI at `/api/swagger/ui`

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">

Built with ❤️ by [Khaled Ben Abderrahim](https://github.com/KhaledBenAbderrahim)

</div>