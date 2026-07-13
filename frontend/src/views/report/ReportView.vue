<script setup>
import { ref, onMounted, computed } from 'vue'
import { FileText, Trash2, Loader2, BookOpen, X, Clock, ChevronLeft, ChevronRight } from '@lucide/vue'
import http from '@/js/http/api.js'

const reports = ref([])
const loading = ref(true)
const showModal = ref(false)
const currentReport = ref(null)
const isDeleting = ref(false)
const deletingId = ref(null)

// 分页
const page = ref(1)
const perPage = 10
const maxPageButtons = 5
const totalPages = computed(() => Math.max(1, Math.ceil(reports.value.length / perPage)))
const pagedReports = computed(() => {
  const start = (page.value - 1) * perPage
  return reports.value.slice(start, start + perPage)
})
const pageRange = computed(() => {
  const total = totalPages.value
  const half = Math.floor(maxPageButtons / 2)
  let s = Math.max(1, page.value - half)
  let e = Math.min(total, s + maxPageButtons - 1)
  if (e - s + 1 < maxPageButtons) s = Math.max(1, e - maxPageButtons + 1)
  const pages = []
  for (let i = s; i <= e; i++) pages.push(i)
  return pages
})

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
  deletingId.value = report.id
  try {
    const res = await http.delete(`/api/reports/${report.id}`)
    if (res.data?.success) {
      reports.value = reports.value.filter(r => r.id !== report.id)
      if (page.value > totalPages.value) page.value = totalPages.value
    }
  } catch (e) { console.error('删除报告失败', e) }
  finally { deletingId.value = null }
}

// Markdown → HTML 渲染
function mdToHtml(text) {
  if (!text) return ''

  // 转义 HTML
  let html = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  // 代码块 ```code``` → 必须优先处理，避免内部 markdown 被二次转换
  const codeBlocks = []
  html = html.replace(/```(\w*)\n?([\s\S]*?)```/g, (_, lang, code) => {
    const idx = codeBlocks.length
    codeBlocks.push(`<pre class="bg-base-300 p-3 rounded-lg overflow-x-auto text-sm my-3"><code>${code.trim()}</code></pre>`)
    return `%%CODEBLOCK_${idx}%%`
  })

  // 内联代码
  html = html.replace(/`([^`]+)`/g, '<code class="bg-base-200 px-1 rounded text-sm">$1</code>')

  // 标题
  html = html.replace(/^#### (.+)$/gm, '<h4 class="font-semibold mt-3 mb-1">$1</h4>')
  html = html.replace(/^### (.+)$/gm, '<h3 class="text-md font-semibold mt-4 mb-2">$1</h3>')
  html = html.replace(/^## (.+)$/gm, '<h2 class="text-lg font-semibold mt-5 mb-2 border-b pb-1">$1</h2>')
  html = html.replace(/^# (.+)$/gm, '<h1 class="text-xl font-bold mt-5 mb-3">$1</h1>')

  // 分隔线
  html = html.replace(/^---$/gm, '<hr class="my-4 border-base-300">')
  html = html.replace(/^\*\*\*$/gm, '<hr class="my-4 border-base-300">')

  // 粗体和斜体
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>')

  // 链接
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener" class="link link-info">$1</a>')

  // 无序列表
  html = html.replace(/^- (.+)$/gm, '<li class="ml-4 list-disc">$1</li>')

  // 有序列表
  html = html.replace(/^\d+\.\s+(.+)$/gm, '<li class="ml-4 list-decimal">$1</li>')

  // 段落（连续两个换行）
  html = html.replace(/\n\n/g, '</p><p class="mb-2">')

  // 单换行（不是段落结束的）
  html = html.replace(/\n/g, '<br>')

  // 恢复代码块
  html = html.replace(/%%CODEBLOCK_(\d+)%%/g, (_, idx) => codeBlocks[parseInt(idx)] || '')

  return '<p class="mb-2">' + html + '</p>'
}

function formatTime(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`
}

function statusBadge(status) {
  if (status === 'completed') return 'bg-success/10 text-success'
  if (['generating','planning','awaiting_confirm'].includes(status)) return 'bg-info/10 text-info'
  return 'bg-warning/10 text-warning'
}
</script>

<template>
  <main class="flex-1 px-5 py-8 max-w-4xl mx-auto w-full">
    <h1 class="text-2xl font-semibold mb-6 flex items-center gap-2">
      <FileText class="w-6 h-6" /> 我的报告
      <span v-if="reports.length" class="text-sm font-normal text-base-content/40">共 {{ reports.length }} 篇</span>
    </h1>

    <div v-if="loading" class="flex justify-center py-16"><Loader2 class="w-6 h-6 animate-spin text-base-content/40" /></div>

    <div v-else-if="reports.length === 0" class="text-center py-16 text-base-content/40">
      <FileText class="w-12 h-12 mx-auto mb-3 opacity-30" />
      <p>暂无报告，进入研究模式发起研究后可查看报告</p>
    </div>

    <template v-else>
      <!-- 报告列表 -->
      <div class="flex flex-col gap-3">
        <div
          v-for="report in pagedReports"
          :key="report.id"
          class="card bg-base-100 shadow-sm border border-base-200 hover:shadow-md transition-shadow cursor-pointer"
          @click="viewReport(report)"
        >
          <div class="card-body py-3 px-5">
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
              <button
                class="btn btn-ghost btn-xs btn-square ml-2 shrink-0"
                @click="deleteReport(report, $event)" title="删除"
                :disabled="deletingId === report.id"
              >
                <Loader2 v-if="deletingId === report.id" class="w-4 h-4 animate-spin text-error" />
                <Trash2 v-else class="w-4 h-4 text-error" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="totalPages > 1" class="flex items-center justify-center gap-1 mt-6">
        <button class="btn btn-ghost btn-sm" :disabled="page <= 1" @click="page = Math.max(1, page - 1)">
          <ChevronLeft class="w-4 h-4" />
        </button>
        <button
          v-for="p in pageRange"
          :key="p"
          class="btn btn-sm min-w-[36px]"
          :class="p === page ? 'btn-neutral' : 'btn-ghost'"
          @click="page = p"
        >{{ p }}</button>
        <button class="btn btn-ghost btn-sm" :disabled="page >= totalPages" @click="page = Math.min(totalPages, page + 1)">
          <ChevronRight class="w-4 h-4" />
        </button>
      </div>
    </template>

    <!-- 报告详情模态框 -->
    <div v-if="showModal && currentReport" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4" @click.self="closeModal">
      <div class="bg-base-100 rounded-lg shadow-2xl w-full max-w-6xl flex flex-col" style="height: 90vh; max-height: 90vh;">
        <!-- 头部 -->
        <div class="flex items-center justify-between px-6 py-3 border-b border-base-200 shrink-0">
          <h2 class="text-lg font-semibold truncate pr-4">{{ currentReport.title }}</h2>
          <button class="btn btn-ghost btn-sm btn-circle shrink-0" @click="closeModal">
            <X class="w-5 h-5" />
          </button>
        </div>
        <!-- 内容（可滚动） -->
        <div class="overflow-y-auto px-6 py-5" style="flex: 1; min-height: 0;">
          <div class="prose prose-sm max-w-none leading-relaxed break-words" v-html="mdToHtml(currentReport.content)"></div>
          <div v-if="currentReport.sources && currentReport.sources.length" class="mt-6 pt-4 border-t border-base-200">
            <h3 class="text-sm font-semibold mb-2">📚 参考资料</h3>
            <div v-for="s in currentReport.sources" :key="s.index" class="text-xs text-base-content/60 py-1 flex items-start gap-2">
              <span class="shrink-0">[{{ s.index }}]</span>
              <a :href="s.url" target="_blank" rel="noopener" class="link link-info break-all">{{ s.title }}</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
