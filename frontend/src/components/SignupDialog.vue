<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import apiAuth from '@/api/auth'

defineProps<{ visible: boolean }>()
const emit = defineEmits<['update:visible']>()

const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)

async function signup() {
  loading.value = true
  try {
    await apiAuth.register({ username: username.value, email: email.value, password: password.value })
    ElMessage.success('Signup successful, please login')
    emit('update:visible', false)
  } catch (err: unknown) {
    ElMessage.error(err.response?.data?.detail || 'Signup failed')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <el-dialog :model-value="visible" title="Sign Up" width="400px">
    <el-form>
      <el-form-item label="Username">
        <el-input v-model="username" />
      </el-form-item>
      <el-form-item label="Email">
        <el-input v-model="email" type="email" />
      </el-form-item>
      <el-form-item label="Password">
        <el-input type="password" v-model="password" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="emit('update:visible', false)">Cancel</el-button>
      <el-button type="primary" :loading="loading" @click="signup">Sign Up</el-button>
    </template>
  </el-dialog>
</template>

