<script>
    import { getFollowContent } from "../api.js";
    import FollowCard from "./FollowCard.svelte";
    import LoadingCard from "./LoadingCard.svelte";
    import { tick } from "svelte";

    export let groq_news;

    let follow_contents = [];

    let follow_content_container;
    let isLoading = false;
    let search_question = "";

    const handleQuestion = async (question, groq_news) => {
        search_question = question;
        isLoading = true;
        await tick();
        follow_content_container.lastChild.scrollIntoView({
            behavior: "smooth",
            block: "end",
            inline: "nearest",
        });
        const new_content = await getFollowContent(question, groq_news);
        follow_contents = [...follow_contents, new_content];
        isLoading = false;
        await tick();
        follow_content_container.lastChild.scrollIntoView({
            behavior: "smooth",
            block: "end",
            inline: "nearest",
        });
    };

    const handleCustomQuestion = async () => {
        console.log("custom question !");
        isLoading = true;
        await tick();
        console.log("search_question", search_question);
        console.log(
            "follow_content_container.lastChild",
            follow_content_container.lastChild,
        );
        follow_content_container.lastChild.scrollIntoView({
            behavior: "smooth",
            block: "end",
            inline: "nearest",
        });
        const new_content = await getFollowContent(search_question);
        follow_contents = [...follow_contents, new_content];
        isLoading = false;
        await tick();
        follow_content_container.lastChild.scrollIntoView({
            behavior: "smooth",
            block: "end",
            inline: "nearest",
        });
    };
</script>

<div
    bind:this={follow_content_container}
    class="card carousel-item w-full rounded-box bg-base-100"
>
    <div class="carousel-vertical">
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
                {#if groq_news.news_source}
                    <div class="badge bg-[#ff7000] text-white p-2 gap-2">
                        <img src={`https://www.google.com/s2/favicons?domain=${groq_news.news_source}`} alt={groq_news.news_source} class="w-4 h-4 border-none rounded-lg" />
                        {new URL(groq_news.news_source).hostname.split(".").reverse()[1]}
                    </div>
                {/if}
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
                            handleQuestion(groq_news.groq_question_1, groq_news)}
                    >
                        {groq_news.groq_question_1}
                        <p class="text-2xl text-right text-[#ff7000]">+</p>
                    </button>
                    <button
                        class="flex border-t-2 pt-1 items-center flex-row text-left transition-all duration-300 hover:text-[#ff7000]"
                        on:click={() =>
                            handleQuestion(groq_news.groq_question_2, groq_news)}
                    >
                        {groq_news.groq_question_2}
                        <p class="text-2xl text-right text-[#ff7000]">+</p>
                    </button>
                    <button
                        class="flex border-t-2 pt-1 items-center flex-row text-left transition-all duration-300 hover:text-[#ff7000]"
                        on:click={() =>
                            handleQuestion(groq_news.groq_question_2, groq_news)}
                    >
                        {groq_news.groq_question_3}
                        <p class="text-2xl text-right text-[#ff7000]">+</p>
                    </button>
                    <form
                        class="flex border-t-2 border-b-[#ff7000] pb-2 pt-4"
                        on:submit={() => {
                            e.preventDefault();
                            handleQuestion(search_question, groq_news);
                        }}
                    >
                        <input
                            type="text"
                            placeholder="Have a question?"
                            class="w-full outline-none text-[#ff7000]"
                            on:change={(e) => search_question = e.target.value}
                        />
                        <button type="submit" class="text-2xl text-[#ff7000]"
                            >+</button
                        >
                    </form>
                </div>
            </div>
        </div>
        {#each follow_contents as follow_content (follow_content.groq_title)}
            <FollowCard
                {follow_content}
                onFollowQuestion={handleQuestion}
                handleCustomQuestion={handleQuestion}
            />
        {/each}
        {#if isLoading}
            <LoadingCard question={search_question} />
        {/if}
    </div>
</div>
