<script setup>
import { ref } from 'vue'
import {
  ZoomIn,
  ZoomOut,
  RotateCw,
  Check,
  X,
  Upload,
  User,
} from '@lucide/vue'
import http from '@/js/http/api.js'
import { useUserStore } from '@/stores/user.js'

const userStore = useUserStore()
const emit = defineEmits(['updated'])

const showEditor = ref(false)
const uploading = ref(false)
const previewUrl = ref('')
const fileInput = ref(null)
const cropContainer = ref(null)

const cropX = ref(0)
const cropY = ref(0)
const zoom = ref(1)
const rotation = ref(0)
const sourceSize = ref({ w: 0, h: 0 })
const origNatural = ref({ w: 0, h: 0 })

const dragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })

const maskSize = 200

function onFileChange(e) {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (ev) => {
    previewUrl.value = ev.target.result
    cropX.value = 0; cropY.value = 0; zoom.value = 1; rotation.value = 0
    showEditor.value = true
  }
  reader.readAsDataURL(file)
}

function onImgLoad(e) {
  const { naturalWidth, naturalHeight } = e.target
  origNatural.value = { w: naturalWidth, h: naturalHeight }
  const scale = maskSize / Math.min(naturalWidth, naturalHeight)
  sourceSize.value = {
    w: Math.round(naturalWidth * scale),
    h: Math.round(naturalHeight * scale),
  }
}

function onDragStart(e) {
  e.preventDefault()
  dragging.value = true
  const pt = e.touches ? e.touches[0] : e
  dragStart.value = { x: pt.clientX, y: pt.clientY }
}
function onDragMove(e) {
  if (!dragging.value) return
  e.preventDefault()
  const pt = e.touches ? e.touches[0] : e
  cropX.value += pt.clientX - dragStart.value.x
  cropY.value += pt.clientY - dragStart.value.y
  dragStart.value = { x: pt.clientX, y: pt.clientY }
}
function onDragEnd() {
  dragging.value = false
}

// 鼠标滚轮缩放，以图片中心为基准（transform-origin: center 已保证）
function onWheel(e) {
  e.preventDefault()
  const step = 0.1
  if (e.deltaY < 0) {
    zoom.value = Math.min(3, zoom.value + step)
  } else {
    zoom.value = Math.max(0.5, zoom.value - step)
  }
}

async function doCrop() {
  const sw = sourceSize.value.w, sh = sourceSize.value.h
  const ow = origNatural.value.w, oh = origNatural.value.h
  const ratio = ow / sw
  const rz = zoom.value

  // 显示尺寸（缩放后）
  const displayW = sw * rz, displayH = sh * rz
  // 图片中心相对 mask 中心的偏移
  const cx = (displayW - maskSize) / 2 + cropX.value
  const cy = (displayH - maskSize) / 2 + cropY.value
  // 转原始坐标
  const x = Math.max(0, Math.round(cx / rz * ratio))
  const y = Math.max(0, Math.round(cy / rz * ratio))
  const size = Math.round(maskSize / rz * ratio)

  const blob = await (await fetch(previewUrl.value)).blob()
  const form = new FormData()
  form.append('file', blob, 'avatar.png')
  form.append('crop_x', String(x))
  form.append('crop_y', String(y))
  form.append('crop_w', String(Math.min(size, ow - x)))
  form.append('crop_h', String(Math.min(size, oh - y)))

  uploading.value = true
  try {
    const res = await http.post('/api/user/avatar', form)
    if (res.data.success) {
      userStore.photo = res.data.data.photo
      emit('updated')
    }
  } catch (e) {
    console.error(e)
  }
  uploading.value = false
  showEditor.value = false
}

function cancelCrop() {
  showEditor.value = false
  previewUrl.value = ''
}
</script>

<template>
  <div class="flex flex-col items-center gap-4">
    <div
      class="avatar cursor-pointer group relative"
      @click="fileInput?.click()"
    >
      <div class="w-32 rounded-full ring ring-base-300">
        <img v-if="userStore.photo" :src="userStore.photo" alt="头像" />
        <div v-else class="w-32 h-32 rounded-full bg-neutral text-neutral-content flex items-center justify-center">
          <User class="w-12 h-12" />
        </div>
      </div>
      <div class="absolute inset-0 flex items-center justify-center bg-black/40 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
        <Upload class="w-6 h-6 text-white" />
      </div>
    </div>

    <p class="text-sm text-base-content/50">点击头像更换</p>

    <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange" />

    <!-- 裁剪弹窗 -->
    <Teleport to="body">
      <div v-if="showEditor" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
        <div class="bg-base-100 rounded-xl p-6 w-[420px] shadow-2xl">
          <h3 class="text-lg font-bold mb-4 text-center">裁剪头像</h3>

          <div class="flex justify-center mb-4">
            <div
              ref="cropContainer"
              class="relative rounded-full overflow-hidden border-2 border-dashed border-base-content/30"
              :style="{ width: maskSize + 'px', height: maskSize + 'px' }"
              @mousedown="onDragStart" @mousemove="onDragMove" @mouseup="onDragEnd" @mouseleave="onDragEnd"
              @touchstart="onDragStart" @touchmove="onDragMove" @touchend="onDragEnd"
              @wheel.prevent="onWheel"
            >
              <img
                v-if="previewUrl"
                :src="previewUrl"
                @load="onImgLoad"
                class="absolute select-none pointer-events-none"
                alt="用户头像"
                :style="{
                  width: sourceSize.w + 'px',
                  height: sourceSize.h + 'px',
                  left: (-(sourceSize.w - maskSize) / 2 + cropX) + 'px',
                  top: (-(sourceSize.h - maskSize) / 2 + cropY) + 'px',
                  transform: 'scale(' + zoom + ') rotate(' + rotation + 'deg)',
                }"
                draggable="false"
              />
            </div>
          </div>

          <div class="flex items-center justify-center gap-4 mb-6">
            <button class="btn btn-sm btn-circle btn-ghost" @click="zoom = Math.max(0.5, zoom - 0.25)">
              <ZoomOut class="w-4 h-4" />
            </button>
            <input type="range" min="0.5" max="3" step="0.05" v-model.number="zoom" class="range range-sm w-32" />
            <button class="btn btn-sm btn-circle btn-ghost" @click="zoom = Math.min(3, zoom + 0.25)">
              <ZoomIn class="w-4 h-4" />
            </button>
            <button class="btn btn-sm btn-circle btn-ghost" @click="rotation = (rotation + 90) % 360">
              <RotateCw class="w-4 h-4" />
            </button>
          </div>

          <div class="flex justify-center gap-4">
            <button class="btn btn-outline" @click="cancelCrop">
              <X class="w-4 h-4" /> 取消
            </button>
            <button class="btn btn-neutral" :disabled="uploading" @click="doCrop">
              <Check class="w-4 h-4" />
              {{ uploading ? '保存中...' : '确认裁剪' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
