<script setup>
import { ref, reactive, onMounted, computed } from "vue";
import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:8000" });


const halaman = ref("login");
const userAktif = ref(null);
const form = reactive({ username: "", password: "" });
const tasks = ref([]);
const teksTugas = ref("");
const fileGambar = ref(null);
const loadingCek = ref(false);
const hasilPrediksi = ref("");

const getAuthHeader = () => ({
  headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
});

const register = async () => {
  try {
    await api.post("/register", form);
    alert("Registrasi Berhasil! Silakan Login.");
    halaman.value = "login";
  } catch (err) {
    alert(err.response?.data?.detail || "Gagal Mendaftar");
  }
};

const login = async () => {
  try {
    const res = await api.post("/login", form);
    const { access_token, user } = res.data;
    userAktif.value = user;
    localStorage.setItem("token", access_token);
    localStorage.setItem("username", user.username);
    await ambilTugas();
    halaman.value = "dashboard";
    form.username = "";
    form.password = "";
  } catch (err) {
    alert("Login Gagal! Periksa kembali akun Anda.");
  }
};

const logout = () => {
  localStorage.clear();
  userAktif.value = null;
  halaman.value = "login";
  tasks.value = [];
  hasilPrediksi.value = "";
  fileGambar.value = null;
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
  previewUrl.value = null;
};

const previewUrl = ref(null);

const handleFileChange = (e) => {
  const file = e.target.files[0];
  if (!file) return;
  fileGambar.value = file;
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
  previewUrl.value = URL.createObjectURL(file);
};

const ambilTugas = async () => {
  try {
    const res = await api.get("/tasks", getAuthHeader());
    tasks.value = res.data;
  } catch (err) {
    console.error("Gagal sinkronisasi data.");
  }
};

const tambahTugas = async () => {
  if (!teksTugas.value.trim()) return;
  try {
    const res = await api.post(
      "/tasks",
      { teks: teksTugas.value },
      getAuthHeader()
    );
    tasks.value.unshift(res.data);
    teksTugas.value = "";
  } catch (err) {
    alert("Gagal menyimpan catatan.");
  }
};

const hapusTugas = async (id) => {
  try {
    await api.delete(`/tasks/${id}`, getAuthHeader());
    tasks.value = tasks.value.filter((t) => t.id !== id);
  } catch (err) {
    alert("Gagal menghapus.");
  }
};

const cekGambar = async () => {
  if (!fileGambar.value) return alert("Pilih gambar medis terlebih dahulu!");
  loadingCek.value = true;
  const formData = new FormData();
  formData.append("file", fileGambar.value);

  try {
    const res = await api.post("/predict", formData);
    hasilPrediksi.value = res.data.prediction;
    teksTugas.value = "Hasil Diagnosa: " + res.data.prediction;
  } catch (err) {
    alert("gagal menganalisis gambar ini.");
  } finally {
    loadingCek.value = false;
  }
};

onMounted(() => {
  const savedUser = localStorage.getItem("username");
  if (savedUser) {
    userAktif.value = { username: savedUser };
    halaman.value = "dashboard";
    ambilTugas();
  }
});
</script>

<template>
  <div class="app-wrapper">
    <div v-if="halaman === 'login' || halaman === 'register'" class="auth-card">
      <div class="brand">
        <h1>Belz<span>classification</span></h1>
        <p>
          {{
            halaman === "login" ? "Portal Diagnosa Medis " : "Buat Akun Baru"
          }}
        </p>
      </div>

      <div class="form-group">
        <input
          v-model="form.username"
          placeholder="Username"
          class="inp"
          @keyup.enter="halaman === 'login' ? login() : register()"
        />
        <input
          v-model="form.password"
          type="password"
          placeholder="Password"
          class="inp"
          @keyup.enter="halaman === 'login' ? login() : register()"
        />
      </div>

      <button
        @click="halaman === 'login' ? login() : register()"
        class="btn-main"
        :class="{ 'btn-reg': halaman === 'register' }"
      >
        {{ halaman === "login" ? "Sign In" : "Create Account" }}
      </button>

      <p class="toggle-text">
        {{ halaman === "login" ? "Belum punya akun?" : "Sudah punya akun?" }}
        <span @click="halaman = halaman === 'login' ? 'register' : 'login'">
          {{ halaman === "login" ? "Daftar di sini" : "Login sekarang" }}
        </span>
      </p>
    </div>

    <div v-else class="dashboard-box">
      <header class="db-header">
        <div class="user-info">
          <h2>Halo, {{ userAktif?.username }}</h2>
        </div>
        <button @click="logout" class="btn-logout">Logout</button>
      </header>

      <div class="ai-box">
        <div v-if="previewUrl" class="image-preview-wrapper">
          <img :src="previewUrl" class="main-preview" />
          <div class="file-name-overlay">{{ fileGambar.name }}</div>
        </div>

        <label class="file-label" :class="{ 'has-file': fileGambar }">
          <input
            type="file"
            @change="handleFileChange"
            hidden
            accept="image/*"
          />
          <span v-if="!fileGambar"> Upload Gambar Medis</span>
          <span v-else> Ganti Gambar</span>
        </label>

        <button
          @click="cekGambar"
          :disabled="loadingCek || !fileGambar"
          class="btn-ai"
        >
          {{ loadingCek ? "Menganalisis..." : "Klasifikasikan Gambar" }}
        </button>
      </div>

      <transition name="fade">
        <div v-if="hasilPrediksi" class="prediction-alert">
          <div class="result-text">
            <strong>Hasil Analisis:</strong> {{ hasilPrediksi }}
          </div>
          <button @click="tambahTugas" class="btn-save">Simpan</button>
        </div>
      </transition>

      <div class="task-list-container">
        <ul class="task-list">
          <li v-for="t in tasks" :key="t.id" class="task-item">
            <span class="task-text">{{ t.teks }}</span>
            <button @click="hapusTugas(t.id)" class="btn-del">🗑️</button>
          </li>
        </ul>
      </div>
      <p class="medical-disclaimer">
        <span>Disclaimer:</span> Klasifikasi ini dibuat hanya sebagai
        diagnosa sementara. Harap lakukan pengecekan lebih lanjut ke dokter
        spesialis.
      </p>
    </div>
  </div>
</template>

<style scoped>

.app-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #0f172a;
  font-family: "Inter", system-ui, sans-serif;
  padding: 20px;
}

.auth-card,
.dashboard-box {
  background: #ffffff;
  padding: 40px;
  border-radius: 24px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.brand {
  text-align: center;
  margin-bottom: 30px;
}
h1 {
  color: #2563eb;
  margin: 0;
  font-weight: 800;
  font-size: 28px;
  letter-spacing: -1px;
}
h1 span {
  color: #334155;
}
.subtitle {
  color: #64748b;
  font-size: 14px;
  margin-top: 5px;
}


.form-group {
  margin-bottom: 20px;
}
.inp {
  width: 100%;
  padding: 14px;
  margin-bottom: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-sizing: border-box;
  font-size: 15px;
  transition: all 0.2s;
}
.inp:focus {
  outline: none;
  border-color: #2563eb;
}


.btn-main {
  width: 100%;
  padding: 14px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-main:hover {
  opacity: 0.9;
}
.btn-reg {
  background: #334155;
}
.toggle-text {
  text-align: center;
  font-size: 14px;
  color: #64748b;
  margin-top: 20px;
}
.toggle-text span {
  color: #2563eb;
  cursor: pointer;
  font-weight: 700;
}

.btn-save {
  background: #1e293b;
  color: #ffffff;
  border: none;
  padding: 8px 18px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-left: auto; 
}

.btn-save:hover {
  background: #0f172a;
  transform: translateY(-1px);
  box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.15);
}

.btn-save:active {
  transform: translateY(0);
}

.prediction-alert-container {
  margin-bottom: 25px;
}

.medical-disclaimer {
  font-size: 11px;
  line-height: 1.5;
  color: #64748b;
  margin-top: 10px;
  padding: 0 5px;
  text-align: justify;
}

.medical-disclaimer span {
  font-weight: bold;
  color: #ff0000;
}

.btn-save {
  background: #ffffff;
  color: #166534;
  border: 1px solid #bbf7d0;
  padding: 6px 14px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.btn-save:hover {
  background: #166534;
  color: #ffffff;
  transform: translateY(-1px);
}

.prediction-alert {
  display: flex;
  align-items: center; 
  justify-content: space-between; 
  padding: 15px 20px;
  background: #dcfce7;
  color: #166534;
  border-radius: 12px;
  border-left: 5px solid #10b981;
}

.db-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 15px;
}
.db-header h2 {
  font-size: 18px;
  margin: 0;
  color: #1e293b;
}
.db-header p {
  font-size: 12px;
  color: #64748b;
  margin: 2px 0 0 0;
}
.btn-logout {
  background: #fee2e2;
  color: #ef4444;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
}

.ai-box {
  margin-bottom: 20px;
}

.ai-box span{
  color: #1e293b;
  font-size: 10px;
  font-weight: bold;
}
.file-label {
  display: block;
  padding: 25px;
  border: 2px dashed #cbd5e1;
  border-radius: 16px;
  text-align: center;
  cursor: pointer;
  margin-bottom: 15px;
  transition: all 0.3s;
}
.file-active {
  border-color: #10b981;
  background: #f0fdf4;
}
.label-content .icon {
  font-size: 24px;
  display: block;
  margin-bottom: 5px;
}
.label-content .text {
  font-size: 13px;
  color: #475569;
}

.btn-ai {
  width: 100%;
  padding: 14px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}
.btn-ai:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.prediction-alert {
  padding: 15px;
  background: #dcfce7;
  color: #166534;
  border-radius: 12px;
  margin-bottom: 20px;
  border-left: 5px solid #10b981;
  font-size: 14px;
}

/* Tasks */
.task-input-group {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}
.task-input-group input {
  flex: 1;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
}
.task-input-group button {
  background: #1e293b;
  color: white;
  border: none;
  padding: 0 15px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.task-list-container {
  max-height: 200px;
  overflow-y: auto;
}
.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #f1f5f9;
  font-size: 14px;
}
.task-text {
  color: #334155;
}
.btn-del {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

.image-preview-wrapper {
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 15px;
  border: 1px solid #e2e8f0;
  position: relative;
  background: #000;
}

.main-preview {
  width: 100%;
  max-height: 250px; 
  display: block;
  object-fit: contain; 
}

.file-name-overlay {
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 11px;
  padding: 4px 10px;
  text-align: center;
}

.file-label.has-file {
  padding: 10px;
  font-size: 12px;
  background: #f1f5f9;
  border-style: solid;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
