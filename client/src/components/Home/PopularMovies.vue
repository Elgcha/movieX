<template>
  <div class='col-2 p-2 h-100 d-inline-block'>
    <div v-if='movie' class='card popular'>
      <img :src="imgSrc" alt="popularmovie" class="img-responsive img-rounded">
      <div class="overlay">
        <h3 class="description">{{ movie.title }}</h3>
      </div>
    </div>
    
  </div>
</template>

<script>
export default {
  name:'PopularMovies',
  props: {
    movie: {
      type: Object,
    }
  },
  computed: {
    imgSrc: function () {
      return 'https://image.tmdb.org/t/p/w500/' + this.movie.poster_path
    }
  },
}
</script>

<style>
.popular {
  position: relative;
}
.popular:hover h4 {
  display: none;
} 
.popular:hover .overlay {
  display: block;
  height: 100%;
}
.popular .overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  overflow: hidden;
  width: 100%;
  height: 0;
  color: #fff;
  background: rgba(0, 0, 0, 0.6);
      -webkit-transition: .6s ease;
      transition: .6s ease;
}
.popular .overlay .description {
  font-size: 20px;
  position: absolute;
  top: 50%;
  left: 50%;
  -webkit-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  text-align: center;
}

.popular img {
  height: 240px;
}
</style>