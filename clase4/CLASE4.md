Seguridad

Do you need to secure your API?
Are you… Secure?
…using private or personalized data? Yes.
…sending sensitive data across the 'wire'?
Are you… Secure?
…using private or personalized data? Yes.
…sending sensitive data across the 'wire'? Yes.
Are you… Secure?
…using private or personalized data? Yes.
…sending sensitive data across the 'wire'? Yes.
…using credentials of any kind?
Are you… Secure?
…using private or personalized data? Yes.
…sending sensitive data across the 'wire'? Yes.
…using credentials of any kind? Yes.
Are you… Secure?
…using private or personalized data? Yes.
…sending sensitive data across the 'wire'? Yes.
…using credentials of any kind? Yes.
…trying to protect against overuse of your servers?
Are you… Secure?
…using private or personalized data? Yes.
…sending sensitive data across the 'wire'? Yes.
…using credentials of any kind? Yes.
…trying to protect against overuse of your servers? Yes.


Protect Your API
- Server Infrastructure Security
• Outside scope of API security
- Secure In-Transit
• SSL is almost always appropriate
• Cost of SSL is worth the expense
- Secure the API itself
• Cross Origin Security
• Authorization/Authentication



Authentication vs. Authorization

Authentication
Who you are
Information to determine identity
Credentials/Claims
Authorization
What you can do
Rules about rights (e.g. Roles, Rights)




Basic Auth
- Easy to implement
- But not secure, unless enforcing SSL
- Risky still
• Sends credentials on every request
• Increases surface area of attacks


JSON Web Tokens (JWTs)
- Industry standard
- Self-contained, small and complete
• User Information
• Claims
• Validation Signature
• Other Information

OAuth
- Use trusted third-party to identify
- You never receive credentials
• User authenticates with third party
• Use token to confirm identity
• Safer for you and user

OAuth
- If you need this level of security,
• Don’t implement it by hand please…
