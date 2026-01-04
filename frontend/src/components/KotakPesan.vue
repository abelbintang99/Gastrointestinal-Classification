<template>
  <div class="card">
    <slot></slot>
  </div>
</template>

<style scoped>
.card {
  border: 2px solid #42b883;
  padding: 20px;
  border-radius: 12px;
  background: #1a1a1a;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  margin-top: 20px;
}
</style>