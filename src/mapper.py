class Mapper:
    def map_tables_to_sources(self, scale, **kwargs):
        """Returns a dict with tabels maped to sources"""
        result = {}
        missing_tables = []
        result.update(
            {
                "lineitem": f"{kwargs['li_source']}.public.{kwargs['li_source'][:-1]}_{scale}_lineitem"
            }
        ) if "li_source" in kwargs else missing_tables.append("lineitem")
        result.update(
            {
                "orders": f"{kwargs['o_source']}.public.{kwargs['o_source'][:-1]}_{scale}_orders"
            }
        ) if "o_source" in kwargs else missing_tables.append("orders")
        result.update(
            {
                "customer": f"{kwargs['c_source']}.public.{kwargs['c_source'][:-1]}_{scale}_customer"
            }
        ) if "c_source" in kwargs else missing_tables.append("customer")
        result.update(
            {
                "part": f"{kwargs['pa_source']}.public.{kwargs['pa_source'][:-1]}_{scale}_part"
            }
        ) if "pa_source" in kwargs else missing_tables.append("part")
        result.update(
            {
                "supplier": f"{kwargs['s_source']}.public.{kwargs['s_source'][:-1]}_{scale}_supplier"
            }
        ) if "s_source" in kwargs else missing_tables.append("supplier")
        result.update(
            {
                "partsupp": f"{kwargs['ps_source']}.public.{kwargs['ps_source'][:-1]}_{scale}_partsupp"
            }
        ) if "ps_source" in kwargs else missing_tables.append("partsupp")
        result.update(
            {
                "nation": f"{kwargs['n_source']}.public.{kwargs['n_source'][:-1]}_{scale}_nation"
            }
        ) if "n_source" in kwargs else missing_tables.append("nation")
        result.update(
            {
                "region": f"{kwargs['r_source']}.public.{kwargs['r_source'][:-1]}_{scale}_region"
            }
        ) if "r_source" in kwargs else missing_tables.append("region")
        return result
