<template>
  <div class="search-result-list-container">
    <div v-for="(result, index) in searchResults" :key="index" class="result-item">
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

defineProps<{ searchResults: SearchResult[] }>();
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

  .header {
    display: flex;
    align-items: center;
    margin-bottom: 0.5rem;

    a {
      color: #34322d;
      text-decoration: none;
      font-size: 0.875rem;
      line-height: 1.25rem;
      font-weight: 500;
      transition: color 0.3s ease;

      &:hover {
        text-decoration: underline;
      }
    }
  }

  .summary-container {
    .summary {
      color: #858481;
      font-size: 0.75rem;
      line-height: 1rem;
      margin-top: 0.125rem;
      word-wrap: break-word;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
    }
  }
}
</style>
