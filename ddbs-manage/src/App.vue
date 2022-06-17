<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <header-container></header-container>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu
                style="min-height: 730px;"
                default-active="article_management"
                class="el-menu-vertical-demo"
                unique-opened
                router>
                <el-menu-item index="article_management">
                    <i class="el-icon-document"></i>
                    <span slot="title">Article Management</span>
                </el-menu-item>
                <el-menu-item index="user_management">
                    <i class="el-icon-user"></i>
                    <span slot="title">User Management</span>
                </el-menu-item>
                <el-menu-item index="popular_rank">
                    <i class="el-icon-medal"></i>
                    <span slot="title">Popular Rank</span>
                </el-menu-item>
                <el-menu-item index="read_record">
                    <i class="el-icon-notebook-1"></i>
                    <span slot="title">Read Record</span>
                </el-menu-item>
            </el-menu>
        </el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Header from "@/components/Header";

export default {
  name: "App",
  components: {
    "header-container": Header
  },
};
</script>

<style>
#app {
  width: 100%;
  height: 100%;
}

body {
    display: block;
    margin: 0px;
}

.header {
  background-color: #409EFF;
  color: #fff;
  line-height: 60px;
}

.main-container {
    margin: 20px auto auto 30px;
}

.page-header {
    font-size: 24px;
}

.page-content {
  margin: 30px auto auto 30px;
}

.label-green {
  color: #7ec084;
}

.label-blue {
  color: #36a0ce;
}

.label-yellow {
  color: #d3ab3d;
}

.label-sliver {
  color: rgb(158, 158, 158);
}
</style>
