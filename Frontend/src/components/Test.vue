<template>
    <div>
        <h1>{{ msg }}</h1>
        <button class="btn btn-primary">Test Button</button>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name:'test',
    data() {
        return {
            msg: ""
        }
    },
    methods : {
        getResponse(){
            const path = 'http://127.0.0.1:5000/test';
            axios.get(path)
            .then ((res) => {
                console.log(res.data)
                this.msg = res.data;
            })
            .catch ((err) => {
                    console.error(err);
            });
        },
    },
    created(){
        this.getResponse();
    }
}
</script>