<script setup>

defineProps(['label', 'warna'])
</script>

<template>
  <button :style="{ backgroundColor: warna }">
    {{ label }}
  </button>
</template>

<style scoped>
button {
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  color: white;
  font-weight: bold;
  cursor: pointer;
  margin: 5px;
}
</style>