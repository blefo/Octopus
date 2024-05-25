<script>
    export let groq_news;
</script>

<div class="card carousel-item w-full rounded-box bg-base-100">
    <figure>
        <img src={groq_news.image_cover} alt="Shoes" class="cover" />
    </figure>
    <div class="card-body">
        <h2 class="card-title">{groq_news.groq_title}</h2>
        <ul class="flex flex-col gap-2 pl-4 list-disc">
            <li>{groq_news.groq_key_point_1}</li>
            <li>{groq_news.groq_key_point_2}</li>
            <li>{groq_news.groq_key_point_3}</li>
        </ul>
        <h3 class="text-left mt-4 font-bold">Want to know more?</h3>
        <div class="flex flex-col gap-1 w-full">
            <button class="flex border-t-2 pt-1 items-center flex-row text-left transition-all duration-300 hover:text-[#ff7000]">
                {groq_news.groq_question_1}
                <p class="text-2xl">+</p>
            </button>
            <button class="flex border-t-2 pt-1 items-center flex-row text-left transition-all duration-300 hover:text-[#ff7000]">
                {groq_news.groq_question_2}
                <p class="text-2xl">+</p>
            </button>
            <div class="flex border-t-2 border-b-[#ff7000] pb-2 pt-4">
                <input type="text" placeholder="Have a question?" class="w-full outline-none text-[#ff7000]" />
                <p class="text-2xl text-[#ff7000]">+</p>
            </div>
        </div>
    </div>
</div>
