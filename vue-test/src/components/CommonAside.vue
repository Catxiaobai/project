<template>
  <el-menu router :default-openeds="['/item']">
    <el-menu-item :index="item.path" v-for="item in noChildren" :key="item.path" @click="clickMenu(item)">
      <i :class="'el-icon-' + item.icon"></i>
      <span slot="title">{{ item.label }}</span>
    </el-menu-item>
    <el-submenu :index="item.path" v-for="item in hasChildren" :key="item.path" @click="clickMenu(item)">
      <template slot="title">
        <i :class="'el-icon-' + item.icon"></i>
        <span style="font-size: 18px;font-weight: bold">{{ item.label }}</span>
      </template>
      <el-menu-item-group class="el-children-menu">
        <el-menu-item :index="subItem.path" v-for="subItem in item.children" :key="subItem.path" @click="clickMenu(subItem)">
          <i :class="'el-icon-s-order'"></i>
          {{ subItem.label }}
        </el-menu-item>
      </el-menu-item-group>
    </el-submenu>
  </el-menu>
</template>

<script>
export default {
  name: 'CommonAside.vue',
  computed: {
    noChildren() {
      return this.asideMenu.filter(item => !item.children)
    },
    hasChildren() {
      return this.asideMenu.filter(item => item.children)
    },
    isCollape() {
      return this.$store.state.tab.isCollapsed
    }
  },
  data() {
    return {
      asideMenu: [
        // {
        //   path: '/',
        //   label: '首页',
        //   name: 'home',
        //   icon: 's-home'
        // },
        {
          path: '/item',
          label: '项目',
          name: 'item',
          icon: 'files',
          children: [
            {
              path: '/itemOne',
              label: '项目一',
              name: 'itemOne'
            },
            {
              path: '/itemTwo',
              label: '项目二',
              name: 'itemTwo'
            }
            // {
            //   path: '/safeVerify',
            //   label: '安全性验证',
            //   name: 'safeVerify',
            //   icon: 'more'
            // },
            // {
            //   path: '/trace',
            //   label: '项目二',
            //   name: 'trace'
            // }
          ]
        }

        // {
        //   path: '/person',
        //   label: '人员',
        //   name: 'person',
        //   icon: 'document'
        // }
      ]
    }
  },
  methods: {
    clickMenu(item) {
      if (this.$route.name !== item.name) {
        this.$router.push({ name: item.name })
      }

      this.$store.commit('selectMenu', item)
    }
  }
}
</script>

<style lang="scss" scoped>
.el-menu {
  height: 100%;
}
.el-menu-item {
  font-size: 16px;
}
.el-children-menu {
  background-color: whitesmoke;
}
</style>

<style lang="scss">
//设置了默认左边框为白色
.el-submenu .el-submenu__title.active {
  border-left: #fff solid 6px;
}
//设置鼠标悬停时el-submenu的样式
.el-submenu .el-submenu__title:hover {
  border-left: #33a2ef solid 6px !important;
  background-color: #e2eff9 !important;
  color: #38b2ff !important;
  i {
    color: #38b2ff;
  }
}
</style>

<style lang="scss">
//设置了默认左边框为白色
.el-menu-item {
  border-left: #fff solid 6px;
}

//设置鼠标悬停时el-menu-item的样式
.el-menu-item:hover {
  border-left: #33a2ef solid 6px !important;
  background-color: #e2eff9 !important;
  color: #38b2ff !important;
  //less语法，实现鼠标悬停时icon变色
  i {
    color: #38b2ff;
  }
}
.el-menu-item.is-active {
  border-left: #33a2ef solid 6px !important;
  background-color: #e2eff9 !important;
  color: #38b2ff !important;
  //less语法，实现鼠标悬停时icon变色
  i {
    color: #38b2ff;
  }
}
</style>
