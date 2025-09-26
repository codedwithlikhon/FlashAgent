<template>
  <div class="search-result-list-container">
    <div class="result-item" v-for="(result, index) in searchResults" :key="index">
      <div class="header">
        <a :href="result.url" target="_blank" rel="noreferrer">{{ result.title }}</a>
      </div>
      <div class="summary-container">
        <span class="summary">{{ result.content }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface SearchResult {
  title: string;
  url: string;
  content: string;
}

const props = defineProps<{ searchResults: SearchResult[] }>();
</script>

<style scoped lang="scss">
.search-result-list-container {
  padding: 0.75rem 1rem;
  max-height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.search-result-list-container::-webkit-scrollbar {
  width: 0;
  height: 0;
}

.result-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.header a {
  color: #111827;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 600;
}

.header a:hover {
  text-decoration: underline;
}

.summary {
  color: #6b7280;
  font-size: 0.85rem;
  line-height: 1.2rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
