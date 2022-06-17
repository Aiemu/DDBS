<template>
  <div class="main-container">
    <div class="page-header">Popular Rank</div>
    <div class="page-content">
      <div style="display: flex; margin-bottom: 30px;">
        <el-select style="width: 135px;" v-model="selectedPeriod" placeholder="请选择">
          <el-option
            v-for="item in periodOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <el-input v-if="selectedPeriod === 'day'" style="width: 150px; margin-left: 20px;" v-model="rankDate" placeholder="dd-mm-yyyy"></el-input>
        <el-input v-else-if="selectedPeriod === 'week'" style="width: 150px; margin-left: 20px;" v-model="rankDate" placeholder="ww-yyyy"></el-input>
        <el-input v-else-if="selectedPeriod === 'month'" style="width: 150px; margin-left: 20px;" v-model="rankDate" placeholder="mm-yyyy"></el-input>
        <el-input style="width: 100px; margin-left: 20px;" v-model="topNum" placeholder="num of articles in rank"></el-input>
        <el-button style="width: 100px; margin-left: 70px;" type="primary" @click="getPopularRank">Go</el-button>
      </div>
      <el-table
        :data="tableData"
        style="width: 95%"
        height="500"
        :border="true"
        :cell-class-name="tableCellClassName">
        <el-table-column label="AID" width="70">
          <template slot-scope="scope">
            <span>{{ scope.row.aid }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Title">
          <template slot-scope="scope">
            <el-tooltip
              class="item"
              effect="dark"
              :content="scope.row.abstract"
              placement="top-start"
            >
              <span style="font-weight: bold; font-style: italic;">{{
                scope.row.title
              }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="Author">
          <template slot-scope="scope">
            <span>{{ scope.row.authors }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Category">
          <template slot-scope="scope">
            <span v-if="scope.row.category === 'science'" class="label-green">
              {{ scope.row.category }}
            </span>
            <span
              v-else-if="scope.row.category === 'technology'"
              class="label-blue"
            >
              {{ scope.row.category }}
            </span>
            <span v-else class="label-yellow">
              {{ scope.row.category }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="Tags">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.articleTags }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Language">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.language }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Operations" width="90">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              @click="getArticleDetail(scope.$index, scope.row)"
            >
              Details
            </el-button>
            <!-- <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
              >删除</el-button
            > -->
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog
      :title="selectedArticle.title"
      :visible.sync="dialogDetail"
      width="70%"
    >
      <div>{{ selectedArticleDetail.content }}</div>
      <div style="display: flex; margin-top: 30px;">
        <div v-for="img in selectedArticleDetail.image" :key="img">
          <el-image
            style="width: 200px; height: 200px"
            :src="$baseURL + img"
            fit="scale-down"
          ></el-image>
        </div>
      </div>
        <video
          style="margin-top: 30px;"
          autoplay
          controls
          width="100%"
          height="500"
          id="videoElement"
        ></video>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogDetail = false">OK</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import qs from "qs";
import flvjs from "flv.js";

export default {
  name: "PopularRank",
  data() {
    return {
      dialogDetail: false,
      selectedArticle: {},
      selectedArticleDetail: {},
      selectedPeriod: "day",
      periodOptions: [
        {
          value: 'day',
          label: 'Daily Rank'
        },
        {
          value: 'week',
          label: 'Weekly Rank'
        },
        {
          value: 'month',
          label: 'Monthly Rank'
        }
      ],
      topNum: 5,
      rankDate: '1-1-2018',
      tableData: []
    };
  },
  created() {
    this.getPopularRank();
  },
  methods: {
    tableCellClassName({ row, column, rowIndex, columnIndex }) {
      if (rowIndex === 0 && columnIndex === 1) {
        return "rank-first";
      } else if (rowIndex === 1 && columnIndex === 1) {
        return "rank-second";
      } else if (rowIndex === 2 && columnIndex === 1) {
        return "rank-third";
      }
      return "";
    },
    createVideo() {
      if (flvjs.isSupported()) {
        var videoElement = document.getElementById("videoElement");
        var flvPlayer = flvjs.createPlayer({
          type: "flv",
          url: this.$baseURL + this.selectedArticleDetail.video //你的url地址
        });
        flvPlayer.attachMediaElement(videoElement);
        flvPlayer.load();
        flvPlayer.play();
      }
    },
    getPopularRank() {
      // period: day/week/month, date: string, num: int
      let data = {
        period: this.selectedPeriod,
        date: this.rankDate,
        num: this.topNum
      };
      this.$axios
        .get("/api/popular_rank?" + qs.stringify(data))
        .then(res => {
          if (res.data.status === "success") {
            console.log("Success: get popular rank", res);
            this.tableData = res.data.data.article;
            this.$message.success("Success: get popular rank");
          } else {
            console.log("Error: get popular rank", res);
            this.$message.error(res.data.msg);
          }
        })
        .catch(error => {
          console.log("Error: get popular rank", error);
          this.$message.error("Error: get popular rank", error);
        });
    },
    getArticleDetail(index, row) {
      this.selectedArticle = this.tableData[index];
      this.dialogDetail = true;
      let data = {
        aid: this.selectedArticle.aid % 1000
      };
      this.$axios
        .get("/api/article/detail?" + qs.stringify(data))
        .then(res => {
          if (res.data.status === "success") {
            console.log("Success: get article detail", res);
            this.selectedArticleDetail = res.data.data.article;
            this.$message.success("Success: get article detail");
            this.createVideo();
          } else {
            console.log("Error: get article detail", res);
            this.$message.error(res.data.msg);
          }
        })
        .catch(error => {
          console.log("Error: get article detail", error);
          this.$message.error("Error: get article detail", error);
        });
    }
  }
};
</script>

<style>
.el-table .rank-first {
  color: rgba(238, 213, 99);
  font-size: 20px;
}

.el-table .rank-second {
  color: rgb(158, 158, 158);
  font-size: 20px;
}

.el-table .rank-third {
  color: rgba(139, 92, 16, 0.7);
  font-size: 20px;
}
</style>
