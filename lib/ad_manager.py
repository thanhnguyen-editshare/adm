import ldap
import ldap.sasl
TYPE = {
    "all": "(objectClass=*)",
    "user": "(objectClass=user)",
    "group": "(objectClass=group)",
}


class LDAPADManager():
    """A driver use ldap to connect to AD"""
    con = None

    def authenticate(self, url, username, password):
        self.con = ldap.initialize(url)
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        auth_tokens = ldap.sasl.gssapi()
        self.con.sasl_gssapi_bind_s(auth_tokens)

    def group_search(self, group_name, is_nested=False, o_type="all"):
        base_dn = "OU=editshare, DC=editshare, DC=local"
        s_type = TYPE[o_type]
        group_query = ""
        if is_nested:
            group_query = f"(memberOf:1.2.840.113556.1.4.1941:=cn={group_name}, {base_dn})"
        else:
            group_query = f"(cn={group_name})"
        search_filter = f"(&{s_type}{group_query})"
        result = self._query(base_dn, search_filter)
        return result

    def _query(self, base_dn, search_filter):
        result = self.con.search_s(base_dn,
                                   ldap.SCOPE_SUBTREE,
                                   search_filter,
                                   ['displayName', "memberOf"])
        items = []
        for dn, member in result:
            items.append({"DN": dn,
                          "name": member.get('displayName'),
                          "memberOf": member.get('memberOf')})
        return items
