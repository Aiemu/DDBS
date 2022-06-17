import Vue from 'vue'
import Router from 'vue-router'
import ArticleManagement from '@/pages/ArticleManagement'
import UserManagement from '@/pages/UserManagement'
import PopularRank from '@/pages/PopularRank'
import ReadRecord from '@/pages/ReadRecord'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/article_management',
      name: 'ArticleManagement',
      component: ArticleManagement
    }, {
      path: '/user_management',
      name: 'UserManagement',
      component: UserManagement
    }, {
      path: '/popular_rank',
      name: 'PopularRank',
      component: PopularRank
    }, {
      path: '/read_record',
      name: 'ReadRecord',
      component: ReadRecord
    }
  ]
})
