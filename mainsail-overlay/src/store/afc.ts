import { defineStore } from 'pinia';
import { useMoonraker } from '@/plugins/moonraker';

export const useAFCStore = defineStore('afc', {
  state: () => ({
    status: 'idle',
    activeSlot: 0,
    slots: [] as any[],
    error: null as string | null,
  }),

  actions: {
    init() {
      const mr = useMoonraker();

      mr.on('notify_afc_status_changed', (payload: any) => {
        this.status = payload.status;
        this.activeSlot = payload.active_slot;
        this.slots = payload.slots;
        this.error = payload.error;
      });

      mr.call('machine.afc.status').then((data: any) => {
        this.status = data.status;
        this.activeSlot = data.active_slot;
        this.slots = data.slots;
        this.error = data.error;
      }).catch(() => {});
    },

    selectSlot(slot: number) {
      return useMoonraker().call('machine.afc.select_slot', { slot });
    },

    load(slot: number) {
      return useMoonraker().call('machine.afc.load', { slot });
    },

    unload() {
      return useMoonraker().call('machine.afc.unload', {});
    },

    resetError() {
      return useMoonraker().call('machine.afc.reset_error', {});
    },
  },
});
