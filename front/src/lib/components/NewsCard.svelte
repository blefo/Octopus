<script>
    import { getFollowContent } from "../api.js";
    import FollowCard from "./FollowCard.svelte";
    import { tick } from 'svelte';

    export let groq_news;

    let follow_contents = [];
    let follow_content_container;

    function scrollIntoView(target) {
        let target_id = "#" + target;
		const el = document.getElementById(target_id);
        console.log(el);
		if (!el) return;
        el.scrollIntoView({
            behavior: 'smooth'
        });
    }

    const handleQuestion = async (question) => {
        console.log(question);
        const new_content = await getFollowContent(question);
        follow_contents = [...follow_contents, new_content];
        await tick();
        follow_content_container.lastChild.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest"});
    };
</script>

<div bind:this={follow_content_container} class="card carousel-item w-full rounded-box bg-base-100">
    <div  class="carousel-vertical">
        <div class="arousel-item">
            <figure>
                <img
                    src={groq_news.image_cover}
                    alt="Shoes"
                    class="object-cover h-48 w-full"
                />
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
                    <button
                        class="flex border-t-2 pt-1 items-center flex-row text-left transition-all duration-300 hover:text-[#ff7000]"
                        on:click={() =>
                            handleQuestion(groq_news.groq_question_1)}
                    >
                        {groq_news.groq_question_1}
                        <p class="text-2xl text-right">+</p>
                    </button>
                    <button
                        class="flex border-t-2 pt-1 items-center flex-row text-left transition-all duration-300 hover:text-[#ff7000]"
                        on:click={() => handleQuestion(groq_news.groq_question_2)}
                    >
                        {groq_news.groq_question_2}
                        <p class="text-2xl text-right">+</p>
                    </button>
                    <div class="flex border-t-2 border-b-[#ff7000] pb-2 pt-4">
                        <input
                            type="text"
                            placeholder="Have a question?"
                            class="w-full outline-none text-[#ff7000]"
                            
                        />
                        <p class="text-2xl text-[#ff7000]">+</p>
                    </div>
                </div>
            </div>
        </div>
        
        {#each follow_contents as follow_content (follow_content.groq_title)}
            <FollowCard follow_content={follow_content} onFollowQuestion={handleQuestion} />
        {/each}
    </div>
</div>
