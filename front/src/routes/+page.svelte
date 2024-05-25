<script>
    import { getNews } from '$lib/api';
    import NewsCard from '$lib/components/NewsCard.svelte';

    let news = [];

    getNews().then(data => {
        news = data;
        console.log(data);
    });
</script>

<div class="flex justify-center items-center">
    <div class="w-full md:max-w-2xl " >
        <div class="w-full carousel ">
            {#each news as news (news.groq_title)}
                <NewsCard groq_news={news}  />
            {/each}
        </div>
    </div>
</div>