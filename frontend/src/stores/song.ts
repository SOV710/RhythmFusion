// stores/song.ts
export const useSongStore = defineStore('song', {
  state: () => ({
    // 只存选中列表
    selected: new Set<number>(),
  }),
  actions: {
    toggleSelect(id: number) {
      if (this.selected.has(id)) {
        this.selected.delete(id)
      } else {
        this.selected.add(id)
      }
    },
    isSelected(id: number) {
      return this.selected.has(id)
    },
    // 如果想做分页缓存，可选：
    // pageCache: {} as Record<number, Song[]>,
    // cachePage(page: number, data: Song[]) { this.pageCache[page] = data },
    // getPage(page: number) { return this.pageCache[page] }
  },
})
