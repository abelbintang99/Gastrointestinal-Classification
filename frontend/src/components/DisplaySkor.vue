<script setup>
// Bagian ini penting! 
// Kita bilang: "Papan ini butuh kiriman data bernama 'nilai'"
defineProps(['nilai'])
</script>

<template>
  <div class="papan">
    <h1>{{ nilai }}</h1>
  </div>
</template>

<style scoped>
.papan {
  background-color: #1abc9c;
  padding: 20px;
  border-radius: 50%; /* Membuat kotak jadi bulat */
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px auto;
  box-shadow: 0 0 20px rgba(26, 188, 156, 0.5);
}
h1 {
  margin: 0;
  font-size: 3rem;
  color: white;
}
</style>