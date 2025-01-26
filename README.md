# EdgeRankSimulator

This project involves developing a system that simulates the EdgeRank algorithm, originally developed by Facebook to determine which posts should be displayed in a user's News Feed.

## Project Description

The EdgeRank algorithm ranks posts based on several factors: user affinity, content score, and time decay. The system calculates these factors to generate a dynamic and personalized News Feed for each user.

### Key Factors

- **User Affinity**: Calculated based on the user's past interactions with the content author, including the type and recency of interactions.
- **Content Score**: Measures the popularity of content based on reactions, comments, and shares.
- **Time Decay**: Older posts lose relevance over time, while newer posts are more likely to be displayed.

### Search Functionality

Users can search for posts by entering keywords. The search results are influenced by both the frequency of keyword occurrences in the posts and the relevance of the content derived from the EdgeRank algorithm. The system returns a maximum of 10 posts per search.

## Features

- **EdgeRank Algorithm Implementation**:
  - Simulates the EdgeRank algorithm to rank posts for logged-in users.
  - Uses a graph to organize user interactions for affinity calculations.
  - Enhances search results ranking using EdgeRank scores.
  - Efficiently searches for keywords in posts using the Trie data structure.
  - Supports serialization of data structures for faster subsequent operations.

- **Types of Interactions**:
  - Reactions (likes, loves, wows, hahas, sads, angrys, special)
  - Comments
  - Shares

- **Autocomplete and Phrase Search**:
  - Offers popular completions for partially entered search queries.
  - Supports phrase search by enclosing text in quotes, showing posts with matching phrases in sequence.

- **User Interface**:
  - Provides a console menu for user login, post browsing, and search.
  - Dynamically calculates and displays the set of posts when the user logs in.

This comprehensive system ensures a realistic simulation of the EdgeRank algorithm while offering an efficient and user-friendly experience.
