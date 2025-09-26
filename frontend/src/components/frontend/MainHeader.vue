<template>
  <header class="header">
    <div class="branding">
      <span class="dot" />
      <h1>FlashAgent Workspace</h1>
    </div>
    <div class="actions">
      <a-button type="primary">Launch Agent</a-button>
      <a-button ghost>Docs</a-button>
    </div>
  </header>
</template>

<script setup lang="ts"></script>

<style scoped lang="scss">
.header {
  background: linear-gradient(135deg, #111827, #1f2937);
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #fff;
}

.branding {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.branding h1 {
  margin: 0;
  font-size: 1.25rem;
  letter-spacing: 0.02em;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #22d3ee;
}

.actions {
  display: flex;
  gap: 0.75rem;
}
</style>
