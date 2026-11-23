# Mana AI Lab Instagram publisher

Daily Telugu-English educational images for `@__all_in__onee`, targeted at 10:00 IST from 22 December 2026 through 22 November 2030. Earlier dates are reserved for the existing queue.

The workflow uses GitHub Actions and the Instagram API. Store the Meta-issued Instagram Login access token as the Actions secret `IG_ACCESS_TOKEN`. Set the repository variable `IG_API_VERSION` to the supported Graph version shown for your Meta app. Only authorize an Instagram professional account with basic and content-publishing access. Never commit credentials. The workflow validates the username before publishing. Renew authorization before token expiry and after any revocation. GitHub scheduled runs can be delayed. Monitor Actions failures and the returned Instagram permalinks.
