# A set of notes on how to integrate Keycloak

## Requirements

* Be able to lock access to certain API if there is no valida token
* Be able to use Swagger UI still
* Be able to run unit and integration tests

**OAuth2** is a specification that defines several ways to handle authentication and authorization. **OpenID Connect** is another specification, based on OAuth2, to make it more interoperable.

OpenAPI defines the `apiKey`, `http`, `oauth2`, `openIdConnect` security schemes. Http with a bearer: a header Authorization with a value of Bearer plus a token

## Keycloak summary

Keycloak provides user federation, strong authentication, user management, fine-grained authorization.
The access token issued by Keycloak is in JWT format. It consists of a header, a payload, and a signature separated by periods.

A realm in Keycloak is equivalent to a tenant. Each realm allows an administrator to create isolated groups of applications and users

## FastAPI and Keycloak

There are different libraries available. We can try to use the bare minimum and leverage FastAPI. [FastAPI ways to support authentication and authorization.](https://fastapi.tiangolo.com/tutorial/security/). FastAPI provides several tools for each of the security schemes in the `fastapi.security` module that simplify using these security mechanisms.

The validity of the token is established by checking:

The token’s signature.
The content of the claims.