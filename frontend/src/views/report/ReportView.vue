<script setup>
import { ref, onMounted } from 'vue'
import { FileText, Trash2, Loader2, BookOpen, Eye, X, Clock } from '@lucide/vue'
import http from '@/js/http/api.js'

const reports = ref([])
const loading = ref(true)
const showModal = ref(false)
const currentReport = ref(null)
const isDeleting = ref(false)

onMounted(fetchReports)

async function fetchReports() {
  loading.value = true
  try {
    const res = await http.get('/api/reports')
    if (res.data?.success) reports.value = res.data.data
  } catch (e) { console.error('获取报告列表失败', e) }
  finally { loading.value = false }
}

async function viewReport(report) {
  try {
    const res = await http.get(`/api/reports/${report.id}`)
    if (res.data?.success) {
      currentReport.value = res.data.data
      showModal.value = true
    }
  } catch (e) { console.error('获取报告详情失败', e) }
}

function closeModal() {
  showModal.value = false
  currentReport.value = null
}

async function deleteReport(report, event) {
  event.stopPropagation()
  if (!confirm(`确定删除报告"${report.title}"吗？`)) return
  try {
    const res = await http.delete(`/api/reports/${report.id}`)
    if (res.data?.success) {
      reports.value = reports.value.filter(r => r.id !== report.id)
    }
  } catch (e) { console.error('删除报告失败', e) }
}

function formatTime(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`
}

function statusBadge(status) {
  if (status === 'completed') return 'bg-success/10 text-success'
  if (status === 'generating' || status === 'planning' || status === 'awaiting_confirm') return 'bg-info/10 text-info'
  return 'bg-warning/10 text-warning'
}
</script>

<template>
  <main class="flex-1 px-5 py-8 max-w-4xl mx-auto w-full">
    <h1 class="text-2xl font-semibold mb-6 flex items-center gap-2">
      <FileText class="w-6 h-6" /> 我的报告
    </h1>

    <!-- 加载中 -->
    <div v-if="loading" class="flex justify-center py-16">
      <Loader2 class="w-6 h-6 animate-spin text-base-content/40" />
    </div>

    <!-- 空状态 -->
    <div v-else-if="reports.length === 0" class="text-center py-16 text-base-content/40">
      <FileText class="w-12 h-12 mx-auto mb-3 opacity-30" />
      <p>暂无报告，进入研究模式发起研究后可查看报告</p>
    </div>

    <!-- 报告列表 -->
    <div v-else class="flex flex-col gap-3">
      <div
        v-for="report in reports"
        :key="report.id"
        class="card card-side bg-base-100 shadow-sm border border-base-200 hover:shadow-md transition-shadow cursor-pointer items-center"
        @click="viewReport(report)"
      >
        <div class="card-body py-4 px-5">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3 min-w-0 flex-1">
              <BookOpen class="w-5 h-5 shrink-0 text-info" />
              <div class="min-w-0 flex-1">
                <p class="font-medium truncate">{{ report.title }}</p>
                <p class="text-xs text-base-content/40 flex items-center gap-1 mt-0.5">
                  <Clock class="w-3 h-3" /> {{ formatTime(report.created_at) }}
                </p>
              </div>
            </div>
            <span class="text-xs px-2 py-0.5 rounded-full shrink-0 ml-3" :class="statusBadge(report.status)">
              {{ report.status === 'completed' ? '已完成' : report.status }}
            </span>
            <button class="btn btn-ghost btn-xs btn-square ml-2 opacity-0 group-hover:opacity-100" @click="deleteReport(report, $event)" title="删除">
              <Trash2 class="w-4 h-4 text-error" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 报告详情模态框 -->
    <div v-if="showModal && currentReport" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="closeModal">
      <div class="card bg-base-100 shadow-xl max-w-3xl w-full max-h-[85vh] flex flex-col">
        <div class="card-body p-0 flex flex-col max-h-full">
          <!-- 头部 -->
          <div class="flex items-center justify-between px-6 py-4 border-b border-base-200 shrink-0">
            <h2 class="text-lg font-semibold truncate pr-4">{{ currentReport.title }}</h2>
            <button class="btn btn-ghost btn-sm btn-circle shrink-0" @click="closeModal">
              <X class="w-5 h-5" />
            </button>
          </div>
          <!-- 内容 -->
          <div class="overflow-y-auto px-6 py-4 flex-1">
            <div class="prose prose-sm max-w-none" v-html="currentReport.content.replace(/\n/g, '<br>')"></div>
            <!-- 参考资料 -->
            <div v-if="currentReport.sources && currentReport.sources.length" class="mt-6 pt-4 border-t border-base-200">
              <h3 class="text-sm font-semibold mb-2">参考资料</h3>
              <div v-for="s in currentReport.sources" :key="s.index" class="text-xs text-base-content/60 py-1">
                [{{ s.index }}] <a :href="s.url" target="_blank" class="link link-info">{{ s.title }}</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
