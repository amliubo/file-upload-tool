<template>
  <div class="app">
    <div style="flex-grow: 1; display: flex; justify-content: flex-end">
      <div class="container">
        <el-badge value="hot" class="item">
          <el-button type="success" @click="navigateTo"
            ><svg-icon iconName="icongongxiangzhongxin" />
            <b>Upload Tool</b></el-button
          >
        </el-badge>
        <el-tag type="success" round>
          <p
            style="
              font-size: 34px;
              font-weight: 300;
              text-align: right;
              font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
              font-style: italic;
              transform: skew(-5deg, -2deg);
              letter-spacing: 1.5px;
              line-height: 1.2;
            "
          >
            Package Tool
          </p>
        </el-tag>
      </div>
    </div>
    <p style="margin: 7px 0 7px 0; font-size: 23px; font-weight: 300">
      👋我们可以帮助你轻易获取各渠道最新Package并提供多种操作供你使用。
    </p>
    <el-input
      v-model="search"
      placeholder="搜索（支持：Branches、Channel、Build Plan、Network、Build Time）"
      class="zoom-input"
      style="margin-top: 0"
    />
    <custom-loading :loading="loading" />
    <el-table
      v-if="!loading"
      :data="filteredData"
      style="font-size: 16px; font-weight: 300"
    >
      <el-table-column prop="os" label="OS" width="47">
        <template v-slot="scope">
          <div>
            <svg-icon
              :className="'italic-large'"
              :color="'#3DDC84'"
              v-if="scope.row.os === '.apk'"
              iconName="iconanzhuo"
            />
            <svg-icon
              :className="'italic-large'"
              :color="'#007AFF'"
              v-else-if="scope.row.os === '.ipa'"
              iconName="iconios"
            />
            <svg-icon
              :className="'italic-large'"
              :color="'#007AFF'"
              v-else-if="scope.row.os === 'wxminigame'"
              iconName="iconweixinxiaochengxu"
            />
            <svg-icon
              :className="'italic-large'"
              :color="'#007AFF'"
              v-else-if="scope.row.os === 'qqminigame'"
              iconName="iconqqxiaochengxu-logo"
            />
            <svg-icon
              :className="'italic-large'"
              :color="'#00A1F1'"
              v-else-if="scope.row.os === 'web'"
              iconName="iconie-browser"
            />
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="branch"
        label="Branche"
        align="center"
        width="130"
      />
      <el-table-column
        prop="channel"
        label="Channel"
        align="center"
        width="120"
      >
        <template v-slot="scope">
          <div
            v-if="
              scope.row.os === 'web' && scope.row.channel === '内网测试网页'
            "
          >
            <el-link
              href="https://sdkapi-q.ggbak.com/gameCenter/enjoy?token=zzk4puUOWCH13TXOOb6AuOgAW4AMEjwTpyPs+B0ai/4bCNlI5c5B97Oa22f9GZTiAulLuWVOud86+EudHyYqXwkOM6JDpfxcIUxjkQLfycPJlUKOsIFo8rjmm1TwWwXg"
              target="_blank"
              type="primary"
              class="link-style"
            >
              {{ scope.row.channel }}
            </el-link>
          </div>
          <div
            v-else-if="
              scope.row.os === 'web' && scope.row.channel === '分支测试网页'
            "
          >
            <el-link
              href="https://sdkapi-q.ggbak.com/gameCenter/enjoy?token=zzk4puUOWCH13TXOOb6AuAGdxfHPoC0xoQ0j3LGo3hd4e/NQFBVhsA3+t68RAgX0AulLuWVOud86+EudHyYqXwkOM6JDpfxcIUxjkQLfycPaA8zFp3ffv+ipUlkm3LFI"
              target="_blank"
              type="primary"
              class="link-style"
            >
              {{ scope.row.channel }}
            </el-link>
          </div>
          <div v-else>
            {{ scope.row.channel }}
          </div>
        </template>
      </el-table-column>

      <el-table-column
        prop="build_plan"
        label="Build Plan"
        align="center"
        width="106"
      />
      <el-table-column
        prop="network"
        label="Network"
        align="center"
        width="94"
      />
      <el-table-column
        prop="build_time"
        label="Build Time"
        align="center"
        width="131"
      >
        <template v-slot="scope">
          <el-tag round type="info" :style="{ fontSize: '13.2px' }">{{
            scope.row.build_time
          }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="operate" label="Operate">
        <template v-slot="scope">
          <div class="operation-row">
            <div class="operation-item">
              <el-button
                plain
                @click="handleDownload(scope.row.jenkins_url)"
                class="link-style"
                size="small"
              >
                <svg-icon iconName="iconjenkins" class="icon-style" />
                Jenkins
              </el-button>
            </div>
            <div
              class="operation-item"
              v-if="
                ['.apk', '.ipa', 'wxminigame', 'qqminigame'].includes(
                  scope.row.os
                )
              "
            >
              <el-popover
                v-if="
                  scope.row.os !== 'wxminigame' && scope.row.os !== 'qqminigame'
                "
                placement="right"
                width="200"
                trigger="hover"
              >
                <template v-slot:reference>
                  <el-button plain size="small" class="link-style"
                    ><svg-icon iconName="iconiconfontscan" class="icon-style" />
                    QR
                  </el-button>
                </template>
                <img :src="scope.row.png_url" class="qr-code" />
              </el-popover>
              <el-tooltip
                v-else
                content="小游戏QR预览时效性 暂不可用。"
                placement="top"
                effect="dark"
              >
                <el-button plain size="small" class="link-style" disabled>
                  <svg-icon iconName="iconiconfontscan" class="icon-style" />
                  QR
                </el-button>
              </el-tooltip>
            </div>
            <div
              class="operation-item"
              v-if="scope.row.os === '.apk' || scope.row.os === '.ipa'"
            >
              <el-button
                size="small"
                plain
                @click="handleDownload(scope.row.package_url)"
                class="link-style"
              >
                <svg-icon iconName="iconxiazai" class="icon-style" />
                {{
                  scope.row.package_url &&
                  scope.row.package_url.endsWith(".apk")
                    ? "DLapk"
                    : "DLipa"
                }}
              </el-button>
            </div>
            <div class="operation-item" v-if="scope.row.os === 'web'">
              <el-input
                v-model="scope.row.user"
                disabled
                size="small"
                class="link-style"
                style="width: 165px"
              >
                <template #prefix>
                  <svg-icon iconName="iconuser" class="icon-style" />
                </template>
              </el-input>
            </div>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import SvgIcon from "@/components/SvgIcon.vue";
export default {
  setup() {
    const loading = ref(true);
    const tableData = ref([]);
    const search = ref("");
    const fetchServerFiles = async () => {
      try {
        const response = await axios.get("/get_build_data");
        tableData.value = Array.isArray(response.data)
          ? response.data
          : [response.data];
      } finally {
        loading.value = false;
      }
    };
    const router = useRouter();
    const navigateTo = () => {
      router.push("/");
    };
    const handleDownload = (url) => {
      window.open(url, "_blank");
    };

    const filteredData = computed(() => {
      if (!search.value) {
        return tableData.value;
      }
      return tableData.value.filter((item) => {
        return (
          item.branch.includes(search.value.toLowerCase()) ||
          item.channel.includes(search.value.toLowerCase()) ||
          item.build_plan.includes(search.value.toLowerCase()) ||
          item.network.includes(search.value.toLowerCase()) ||
          item.build_time.includes(search.value.toLowerCase())
        );
      });
    });

    onMounted(() => {
      fetchServerFiles();
    });

    return {
      SvgIcon,
      loading,
      tableData,
      search,
      filteredData,
      navigateTo,
      handleDownload,
    };
  },
};
</script>
<style scoped>
.app {
  width: 50%;
  margin: 0 auto;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

:deep(.el-table th) {
  color: #ff7f7f;
}

:deep(.el-table th .cell) {
  background-color: #f0f0f0;
}

.zoom-input {
  margin-bottom: 4px;
  height: 40px;
}

.zoom-input:hover {
  transform: scale(1.05);
}

.zoom-input {
  transition: transform 0.3s ease;
  border-radius: 10px;
}

.zoom-input:hover {
  transform: scale(1.03);
}

.container {
  display: flex;
  justify-content: space-between;
}

.qr-code {
  width: 100%;
  margin: 0 auto;
}

.italic-large {
  transform: scale(1.7) skewX(-10deg);
  width: 2em;
  height: 2em;
  display: inline-block;
}

.icon-style {
  font-size: 20px;
  margin-right: 1px;
}

.operation-row {
  display: flex;
  flex-wrap: nowrap;
}

.operation-item {
  white-space: nowrap;
  margin-right: 5px;
}

.link-style {
  display: inline-flex;
  font-size: 16px;
  font-weight: 300;
}
</style>
