import ldap
import ldif
import sys
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


def filter_group(
        *,
        group_name,
        ad_conn,
        basedn
):
    searchFilter = "(&(objectCategory=group)(objectClass=group) \
                    (memberOf:1.2.840.113556.1.4.1941:=cn={group_name}, \
                    OU=editshare, DC=esdemo, DC=editshare, DC=com))" \
                    .replace('{group_name}', group_name)
    try:
        list_nested_group = []
        results = ad_conn.search_s(basedn, ldap.SCOPE_SUBTREE, searchFilter)
        if len(results[0]) >= 2 and 'member' in results[0][1]:
            members_tmp = results[0][1]['member']
            for m in members_tmp:
                list_nested_group.append(m.decode("utf-8"))
        return list_nested_group
    except ldap.LDAPError as e:
        logger.error("Error", e)
    finally:
        ad_conn.unbind_s()


def authenticate(address, username, password):
    conn = ldap.initialize('ldap://' + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    try:
        conn.simple_bind_s(username, password)
    except ldap.INVALID_CREDENTIALS:
        return "Invalid credentials"
    except ldap.SERVER_DOWN:
        return "Server down"
    except ldap.LDAPError as e:
        if type(e.message) == dict and e.message.has_key('desc'):
            return "Other LDAP error: " + e.message['desc']
        else:
            return "Other LDAP error: " + e
    logger.info("Connect successfull")
    return conn
