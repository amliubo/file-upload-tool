<template>
  <div class="app">
    <div style="flex-grow: 1; display: flex; justify-content: flex-end">
      <div class="container">
        <el-badge value="new" class="item">
          <el-button type="primary" @click="navigateTo('/')">
            <b>↕️ Upload Tool</b>
          </el-button>
          <el-button type="primary" @click="navigateTo('/pkg')">
            <b>📦 Package Tool</b>
          </el-button>
        </el-badge>
        <el-tag type="primary" round>
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
            Mj Match
          </p>
        </el-tag>
      </div>
    </div>
    <div id="chart" class="chart-container"></div>
    <p></p>
    <div style="width: 90%; margin: 0 auto">
      <el-table :data="sortedData" style="width: 100%" border>
        <el-table-column prop="room" label="房间" width="140"></el-table-column>
        <el-table-column prop="match_time" label="匹配时长 (秒)" width="550">
          <template #default="scope">
            <span style="font-weight: bold">
              {{ scope.row.match_time.join("&nbsp;&nbsp;&nbsp;") }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="date" label="匹配日期">
          <template #default="scope">
            {{ new Date(scope.row.date).toLocaleDateString() }}
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>


<script>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import * as echarts from "echarts";
import SvgIcon from "@/components/SvgIcon.vue";

export default {
  setup() {
    const router = useRouter();
    const navigateTo = (path) => {
      router.push({ path });
    };

    const sortedData = ref([]);

    const fetchMatchStats = async () => {
      try {
        const response = await axios.get("/match");
        return response.data.stats;
      } catch (error) {
        console.error("Error fetching match stats:", error);
        return [];
      }
    };

    const initChart = async () => {
      const stats = await fetchMatchStats();
      console.log("Received stats:", stats);

      if (!stats || !stats.length) {
        console.error("No stats data available.");
        return;
      }

      const chartDom = document.getElementById("chart");
      const myChart = echarts.init(chartDom);

      // 处理数据，确保最近的日期在右侧
      const roomStats = {};

      stats.forEach((item) => {
        const itemDate = new Date(item.date).toISOString().split("T")[0];
        if (!roomStats[item.room]) {
          roomStats[item.room] = [];
        }
        roomStats[item.room].push({
          date: itemDate,
          avg_time: item.avg_time,
          min_time: item.min_time,
          max_time: item.max_time,
        });
      });

      // **确保日期顺序是正确的（从过去到现在，最近的在右侧）**
      let dates = [
        ...new Set(
          stats.map((item) => new Date(item.date).toISOString().split("T")[0])
        ),
      ];
      dates.sort((a, b) => new Date(a) - new Date(b)); // **按日期升序排列**

      const seriesData = [];

      Object.keys(roomStats).forEach((room) => {
        const data = roomStats[room];
        const avgTimes = [];

        dates.forEach((date) => {
          const record = data.find((item) => item.date === date);
          avgTimes.push(record ? record.avg_time : null); // 没有数据时补 null，防止断点
        });

        seriesData.push({
          name: `${room} 平均匹配时间`,
          type: "line",
          data: avgTimes,
        });
      });

      // **配置 ECharts 选项**
      const option = {
        title: {
          text: "自动化匹配时长统计",
          left: "center",
          textStyle: { fontSize: 24, fontWeight: "bold" },
        },
        tooltip: { trigger: "axis" },
        legend: { data: seriesData.map((item) => item.name), top: "10%" },
        grid: { top: "28%", left: "10%", right: "5%", bottom: "10%" },
        xAxis: {
          type: "category",
          data: dates,
          axisLabel: {
            formatter: (value) => echarts.format.formatTime("yy-MM-dd", value),
            rotate: 45, // **斜着展示，防止重叠**
          },
        },
        yAxis: { type: "value", name: "时间 (秒)" },
        series: seriesData,
      };

      myChart.setOption(option);
    };

    const updateSortedData = async () => {
      const stats = await fetchMatchStats();
      sortedData.value = stats.sort(
        (a, b) => new Date(b.date) - new Date(a.date)
      );
    };

    onMounted(() => {
      initChart();
      updateSortedData();
    });

    return {
      SvgIcon,
      navigateTo,
      sortedData,
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

.chart-container {
  width: 100%;
  height: 500px;
  margin-top: 10px;
}
</style>
