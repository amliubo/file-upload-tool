<template>
  <svg :class="svgClass" aria-hidden="true">
    <use :xlink:href="iconClassName" :fill="color" />
  </svg>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps({
  iconName: {
    type: String,
    required: true,
  },
  className: {
    type: String,
    default: "",
  },
  color: {
    type: String,
    default: "#409eff",
  },
});

const iconClassName = computed(() => `#${props.iconName}`);
const svgClass = computed(() => `svg-icon ${props.className}`);
</script>

<style scoped>
.svg-icon {
  width: 1em;
  height: 1em;
  fill: currentColor;
  vertical-align: -2px;
}
</style>