<div align="center">

<style>
@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.gradient-animate {
  background-size: 200% 200%;
  animation: gradient 15s ease infinite;
}

.hover-float:hover {
  transform: translateY(-5px);
  transition: transform 0.3s ease;
}

.hover-scale:hover {
  transform: scale(1.02);
  transition: transform 0.3s ease;
}

.hover-glow:hover {
  box-shadow: 0 0 20px rgba(0, 255, 157, 0.5);
  transition: box-shadow 0.3s ease;
}

.floating {
  animation: float 6s ease-in-out infinite;
}

.pulsing {
  animation: pulse 2s ease-in-out infinite;
}
</style>

<div style="background: linear-gradient(45deg, #1e3c72, #2a5298); padding: 20px; border-radius: 15px; margin: 20px 0;" class="gradient-animate hover-glow">

# 📚 BookBrain-Azure

<div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0;" class="hover-float">
  <img src="https://img.shields.io/badge/azure%20functions-%230062CC.svg?style=for-the-badge&logo=azure-functions&logoColor=white">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/OpenAI-%23412991.svg?style=for-the-badge&logo=openai&logoColor=white">
</div>

<p style="font-size: 1.2em; color: #ffffff; font-style: italic; margin: 15px 0;" class="floating">
  An advanced serverless platform that revolutionizes educational content processing and study analytics.
</p>

<div style="background: rgba(255, 255, 255, 0.15); padding: 10px; border-radius: 8px; display: inline-block;" class="hover-scale pulsing">
  <p style="margin: 0; color: #ffffff;">
    <b>Developed by <a href="https://github.com/KhaledBenAbderrahim" style="color: #00ff9d; text-decoration: none;">Khaled Ben Abderrahim</a></b>
  </p>
</div>

</div>

<div style="background: linear-gradient(135deg, #000428, #004e92); padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2);" class="gradient-animate hover-glow">

## 🚀 Key Features

<div style="padding: 10px; background: rgba(255, 255, 255, 0.1); border-radius: 10px;" class="hover-scale">
  <img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20bookBrain%20features.png" width="80%" style="border-radius: 8px;">
</div>
</div>

<div style="background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d); padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2);" class="gradient-animate hover-glow">

## 💻 Tech Stack

<table align="center" style="background: rgba(255, 255, 255, 0.1); border-radius: 10px; margin: 10px 0;">
<tr>
<td align="center" style="padding: 15px;">
<div style="background: rgba(255, 255, 255, 0.15); padding: 10px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;" class="hover-float">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/azure/azure-original.svg" width="40" height="40"/>
</div>
<br>Azure Functions
</td>
<td align="center" style="padding: 15px;">
<div style="background: rgba(255, 255, 255, 0.15); padding: 10px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;" class="hover-float">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="40" height="40"/>
</div>
<br>Python
</td>
<td align="center" style="padding: 15px;">
<div style="background: rgba(255, 255, 255, 0.15); padding: 10px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;" class="hover-float">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg" width="40" height="40"/>
</div>
<br>PostgreSQL
</td>
<td align="center" style="padding: 15px;">
<div style="background: rgba(255, 255, 255, 0.15); padding: 10px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;" class="hover-float">
<img src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/openai.svg" width="40" height="40"/>
</div>
<br>OpenAI
</td>
</tr>
</table>
</div>

<div style="background: linear-gradient(135deg, #16222A, #3A6073); padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2);" class="gradient-animate hover-glow">

## 🔧 Components

<table style="background: rgba(255, 255, 255, 0.1); border-radius: 10px; margin: 10px 0;">
<tr>
<td width="50%" style="padding: 15px;">
<div style="background: rgba(255, 255, 255, 0.15); padding: 15px; border-radius: 10px;" class="hover-scale">

### 1. PDF Chunking Function
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20pdf%20chunking%20function.png" width="100%" style="border-radius: 8px;">
</div>
</td>
<td width="50%" style="padding: 15px;">
<div style="background: rgba(255, 255, 255, 0.15); padding: 15px; border-radius: 10px;" class="hover-scale">

### 2. Study Progress Function
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20Study%20progress%20function.png" width="100%" style="border-radius: 8px;">
</div>
</td>
</tr>
<tr>
<td width="50%" style="padding: 15px;">
<div style="background: rgba(255, 255, 255, 0.15); padding: 15px; border-radius: 10px;" class="hover-scale">

### 3. Upload Book Function
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20upload%20book%20function.png" width="100%" style="border-radius: 8px;">
</div>
</td>
<td width="50%" style="padding: 15px;">
<div style="background: rgba(255, 255, 255, 0.15); padding: 15px; border-radius: 10px;" class="hover-scale">

### 4. Hourly Study Digest
<img src="https://github.com/KhaledBenAbderrahim/CSRD/blob/main/images/chunk%20_%20Hourly%20Study%20Digest.png" width="100%" style="border-radius: 8px;">
</div>
</td>
</tr>
</table>
</div>

<div style="background: linear-gradient(135deg, #0F2027, #203A43, #2C5364); padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2);" class="gradient-animate hover-glow">

## ⚙️ Setup & Configuration

<details style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0;" class="hover-scale">
<summary style="cursor: pointer; color: #00ff9d; font-weight: bold;">📝 Installation Steps</summary>

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

<details style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0;" class="hover-scale">
<summary style="cursor: pointer; color: #00ff9d; font-weight: bold;">🔑 Environment Variables</summary>

Required environment variables (see `.env.example`):
- `AZURE_STORAGE_CONNECTION_STRING`: Azure Storage connection string
- `DB_HOST`: Database host
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
</details>
</div>

<div style="background: linear-gradient(135deg, #4B79A1, #283E51); padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2);" class="gradient-animate hover-glow">

## 🎯 Target Users

<table align="center" style="background: rgba(255, 255, 255, 0.1); border-radius: 10px; margin: 10px 0;">
<tr>
<td align="center" style="padding: 15px; background: rgba(255, 255, 255, 0.15); border-radius: 8px; margin: 5px;" class="hover-float">📚 Educational Institutions</td>
<td align="center" style="padding: 15px; background: rgba(255, 255, 255, 0.15); border-radius: 8px; margin: 5px;" class="hover-float">💻 E-Learning Platforms</td>
<td align="center" style="padding: 15px; background: rgba(255, 255, 255, 0.15); border-radius: 8px; margin: 5px;" class="hover-float">👨‍🎓 Students and Educators</td>
</tr>
<tr>
<td align="center" style="padding: 15px; background: rgba(255, 255, 255, 0.15); border-radius: 8px; margin: 5px;" class="hover-float">📖 Content Publishers</td>
<td align="center" style="padding: 15px; background: rgba(255, 255, 255, 0.15); border-radius: 8px; margin: 5px;" class="hover-float">🏫 Learning Management Systems</td>
<td align="center" style="padding: 15px; background: rgba(255, 255, 255, 0.15); border-radius: 8px; margin: 5px;" class="hover-float">📱 Educational Apps</td>
</tr>
</table>
</div>

<div style="background: linear-gradient(135deg, #000046, #1CB5E0); padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2);" class="gradient-animate hover-glow">

## 📚 API Documentation

<div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0;" class="hover-scale">
API documentation is available via Swagger UI at <code style="background: rgba(255, 255, 255, 0.15); padding: 3px 8px; border-radius: 4px;">/api/swagger/ui</code>
</div>
</div>

<div style="background: linear-gradient(135deg, #000000, #434343); padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2);" class="gradient-animate hover-glow">

## 📄 License

<div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0;" class="hover-scale">
This project is licensed under the MIT License - see the LICENSE file for details.
</div>
</div>

<div style="background: linear-gradient(45deg, #1e3c72, #2a5298); padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2);" class="gradient-animate hover-glow">

---

<p style="color: #ffffff; font-size: 1.2em; margin: 10px 0;" class="floating">Built with ❤️ by</p>
<a href="https://github.com/KhaledBenAbderrahim" style="color: #00ff9d; font-size: 1.3em; text-decoration: none; font-weight: bold;" class="hover-scale pulsing">Khaled Ben Abderrahim</a>

</div>

</div>