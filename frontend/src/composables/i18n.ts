import { computed, ref } from 'vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import en from 'element-plus/dist/locale/en.mjs'

const language = ref('zh-cn')
const locale = computed(() => (language.value === 'zh-cn' ? zhCn : en))

const toggleI18n = () => {
  language.value = language.value === 'zh-cn' ? 'en' : 'zh-cn'
}

export function useI18n() {
  return { locale, toggleI18n }
}
