<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import apiAuth from '@/api/auth'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

defineProps<{ visible: boolean }>()
const emit = defineEmits<['update:visible']>()

const username = ref('')
const password = ref('')
const loading = ref(false)

const userStore = useUserStore()
const router = useRouter()

async function login() {
  loading.value = true
  try {
    const resp = await apiAuth.login({ username: username.value, password: password.value })
    const { access, refresh } = resp.data
    userStore.setTokens(access, refresh)
    ElMessage.success('Login successful')
    emit('update:visible', false)
    router.push('/')
  } catch (err: unknown) {
    ElMessage.error(err.response?.data?.detail || 'Login failed')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <el-dialog :model-value="visible" title="Login" width="400px">
    <el-form>
      <el-form-item label="Username">
        <el-input v-model="username" autocomplete="username" />
      </el-form-item>
      <el-form-item label="Password">
        <el-input type="password" v-model="password" autocomplete="current-password" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="emit('update:visible', false)">Cancel</el-button>
      <el-button type="primary" :loading="loading" @click="login">Login</el-button>
    </template>
  </el-dialog>
</template>
