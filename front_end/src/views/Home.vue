<template>
  <div class="home">
    <div class="page-area">
      <el-input placeholder="请输入内容" v-model="inputValue" class="search">
        <el-button slot="append" icon="el-icon-search" @click="handleSearchClick"></el-button>
      </el-input>
      <section class="img-area">
        <transition name="el-fade-in-linear">
          <div class="img-contaienr" v-show="imgs.length">
              <div class="img-item" v-for="item in imgs" :key="item.id" @mouseover="() => handleImageHover(item)" @mouseout="() => handleImageOut(item)">
                <el-image :src="item.src">
                  <div slot="placeholder" class="image-slot">
                    <!-- loading<span class="dot">...</span> -->
                  </div>
                </el-image>
                <div class="img-hover-info" v-show="item.isHover">{{ item.desc }}</div>
              </div>
          </div>
        </transition>
      </section>
      <el-button class="footer-btn" icon="el-icon-refresh-right" circle @click="refreshClick"></el-button>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'home',
  components: {
  },
  data() {
    return {
      imgs: [],
      inputValue: ''
    }
  },
  mounted() {
    setTimeout(() => {
      this.imgs = [
        {id: 1, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '我是你爹' },
        {id: 2, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '我是你爹'  },
        {id: 3, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '我是你爹'  },
        {id: 4, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '我是你爹'  },
        {id: 5, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '我是你爹'  },
        {id: 6, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '我是你爹'  },
        {id: 7, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '我是你爹'  },
        {id: 8, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '我是你爹'  },
        {id: 9, src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg', desc: '我是你爹'  }
      ]
    }, 300);
  },
  methods: {
    refreshClick() {
      location.reload()
    },
    handleSearchClick() {
      const arr = this.imgs.concat(this.imgs)
      this.imgs = arr
    },
    handleImageHover(item) {
      this.$set(item,'isHover',true)
    },
    handleImageOut(item) {
      this.$set(item,'isHover',false)
    }
  }
}
</script>

<style lang="less" scoped>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  .page-area {
    width: 1280px;
    .search {
      width: 500px;
    }
    .img-area {
      min-height: 700px;
      .img-contaienr {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        margin-top: 80px;
        .img-item {
          width: 380px;
          margin: 0px 2px;
          position: relative;
          .img-hover-info {
            width: 380px;
            height: 253px;
            position: absolute;
            top: 0px;
            left: 0px;
            background: rgba(0, 0, 0, .5);
            text-align: center;
            line-height: 253px;
            color: #FFF;
          }
        }
      }
    }
  }
  .footer-btn {
    margin-top: 30px;
  }
}
</style>
