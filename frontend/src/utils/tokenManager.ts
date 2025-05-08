// import axios from 'axios'
//
// type Tokens = { access: string; refresh: string }
//
// const KEY_ACCESS = 'access_token'
// const KEY_REFRESH = 'refresh_token'
//
// const isRefreshing = false
// const refreshPromise: Promise<void> | null = null
//
// // 获取／存储 token
// function getAccess(): string | null {
//   return localStorage.getItem(KEY_ACCESS)
// }
// function getRefresh(): string | null {
//   return localStorage.getItem(KEY_REFRESH)
// }
// function setAccess(token: string): void {
//   localStorage.setItem(KEY_ACCESS, token)
// }
//
// /**
//  * 调用 /api/user/verify/ 检查 access 是否有效
//  * 失效时自动调用 /api/user/refresh/ 拿新 access
//  */
// async function verifyAndRefresh(): Promise<void> {
//   if (isRefreshing) {
//     // 如果已有一次刷新在跑，直接等待
//     return refreshPromise!
//   }
//
//   const access = getAccess()
//   if (!access) {
//     throw new Error('no-access-token')
//   }
//
//   isRefreshing = true
//   refreshPromise = (async () => {
//     try {
//       // 1. 验证
//       await axios.post(
//         '/api/user/verify/',
//         { token: access },
//         { baseURL: import.meta.env.VITE_API_BASE_URL, withCredentials: true },
//       )
//       // 验证通过，不做任何事
//     } catch {
//       // 2. 如果 /verify/ 返回 401，再走一次刷新
//       const refresh = getRefresh()
//       if (!refresh) throw new Error('no-refresh-token')
//
//       const { data } = await axios.post<Tokens>(
//         '/api/user/refresh/',
//         { refresh },
//         { baseURL: import.meta.env.VITE_API_BASE_URL, withCredentials: true },
//       )
//       setAccess(data.access)
//     } finally {
//       isRefreshing = false
//       refreshPromise = null
//     }
//   })()
//
//   return refreshPromise
// }
// /**
//  * 启动一个定时器，每隔 N 秒调用一次 verifyAndRefresh
//  * @param intervalSec 间隔秒数，建议 < access 有效期的一半
//  */
// export function startTokenScheduler(intervalSec = 240): void {
//   // 立即执行一次
//   verifyAndRefresh().catch(() => {
//     /* silent */
//   })
//   // 周期执行
//   setInterval(() => {
//     verifyAndRefresh().catch(() => {
//       /* silent */
//     })
//   }, intervalSec * 1000)
// }
//
// // 应用启动时调用
// startTokenScheduler()
