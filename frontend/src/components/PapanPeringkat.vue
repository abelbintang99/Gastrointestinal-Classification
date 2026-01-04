<script setup>
// Komponen ini hanya butuh kiriman data list
defineProps(['daftar'])
</script>

<template>
  <div class="riwayat-section">
    <h3>🏆 Papan Peringkat:</h3>
    <ul>
      <li v-for="(item, index) in daftar" :key="index">
        <b style="color: gold">{{ item.nama }}</b> 
        berhasil menang dengan skor 
        <b style="color: #42b883">{{ item.skor }}</b> 
        <small style="color: grey">[{{ item.waktu }}]</small>
      </li>
    </ul>
    <p v-if="daftar.length === 0">Belum ada pemenang yang tercatat.</p>
  </div>
</template>

<style scoped>
.riwayat-section {
  margin-top: 20px;
  text-align: left;
  background: #2a2a2a;
  padding: 15px;
  border-radius: 8px;
}
ul { list-style: none; padding: 0; }
li { padding: 8px 0; border-bottom: 1px solid #444; }
</style>