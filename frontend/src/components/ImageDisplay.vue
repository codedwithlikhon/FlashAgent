<template>
  <div class="image-container">
    <img v-if="formattedImageData" :src="formattedImageData" alt="Displaying image" />
    <div v-else class="image-placeholder">No image data</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  content: {
    type: Array as () => string[],
    required: true
  },
  imageType: {
    type: String,
    default: 'image/jpeg'
  }
});

const formattedImageData = computed(() => {
  if (!props.content || props.content.length === 0) {
    return '';
  }
  const base64Data = props.content[props.content.length - 1];
  if (!base64Data) {
    return '';
  }
  if (base64Data.startsWith('data:')) {
    return base64Data;
  }
  return `data:${props.imageType};base64,${base64Data}`;
});
</script>

<style scoped lang="scss">
.image-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;

  img {
    max-width: 100%;
    height: auto;
    object-fit: contain;
    border: 1px solid #dadada;
    border-radius: 4px;
    background-color: #fff;
  }

  .image-placeholder {
    color: #888;
    font-size: 0.875rem;
  }
}
</style>
