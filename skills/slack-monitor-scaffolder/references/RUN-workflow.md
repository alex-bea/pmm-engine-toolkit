# Slack monitor scaffolding workflow

1. Gather the monitoring question, approved workspace/channel supplied at runtime, time
   window, keywords, exclusions, evidence fields, output path, and retention policy.
2. Copy the config template without inserting real identifiers into the skill package.
3. Generate a prompt that returns source timestamp, author label, signal, relevance,
   confidence, and follow-up.
4. Default to dry-run, local output, and no reactions, replies, DMs, or posts.
5. Test with synthetic message exports.
6. Obtain approval before connecting, scheduling, or changing external state.
