<template>
  <div class="afc card">
    <div class="card-header">
      <h3>AFC</h3>
      <span class="status">{{ state.status }}</span>
    </div>

    <div class="slots">
      <button
        v-for="slot in state.slots"
        :key="slot.index"
        class="slot"
        :class="{ active: slot.index === state.activeSlot }"
        :style="{ borderColor: slot.color }"
        @click="select(slot.index)"
      >
        <div>{{ slot.name }}</div>
        <small>{{ slot.material }}</small>
      </button>
    </div>

    <div class="actions">
      <button @click="load">Load</button>
      <button @click="unload">Unload</button>
      <button v-if="state.error" class="error" @click="resetError">Reset Error</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useAFCStore } from '@/store/afc';

const afc = useAFCStore();
onMounted(() => afc.init());

const state = computed(() => afc.$state);

function select(slot: number) {
  afc.selectSlot(slot);
}

function load() {
  afc.load(state.value.activeSlot);
}

function unload() {
  afc.unload();
}

function resetError() {
  afc.resetError();
}
</script>

<style scoped>
.afc { padding: 1rem; }
.slots { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.slot { padding: 0.5rem; border: 2px solid #666; border-radius: 4px; }
.slot.active { border-color: white; }
.actions { margin-top: 0.75rem; display: flex; gap: 0.5rem; }
.error { background: #c00; color: white; }
</style>
