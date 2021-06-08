class Mapper:
    def map_tables_torderss(self, scale, **kwargs):
        """Returns a dict with tabels maped to sources"""
        result = {}
        missing_tables = []
        result.update(
            {
                "lineitem": f"{kwargs['lineitem']}.public.{kwargs['lineitem'][:-1]}_{scale}_lineitem"
            }
        ) if "lineitem" in kwargs else missing_tables.append("lineitem")
        result.update(
            {
                "orders": f"{kwargs['orders']}.public.{kwargs['orders'][:-1]}_{scale}_orders"
            }
        ) if "orders" in kwargs else missing_tables.append("orders")
        result.update(
            {
                "customer": f"{kwargs['customer']}.public.{kwargs['customer'][:-1]}_{scale}_customer"
            }
        ) if "customer" in kwargs else missing_tables.append("customer")
        result.update(
            {"part": f"{kwargs['part']}.public.{kwargs['part'][:-1]}_{scale}_part"}
        ) if "part" in kwargs else missing_tables.append("part")
        result.update(
            {
                "supplier": f"{kwargs['supplier']}.public.{kwargs['supplier'][:-1]}_{scale}_supplier"
            }
        ) if "supplier" in kwargs else missing_tables.append("supplier")
        result.update(
            {
                "partsupp": f"{kwargs['partsupp']}.public.{kwargs['partsupp'][:-1]}_{scale}_partsupp"
            }
        ) if "partsupp" in kwargs else missing_tables.append("partsupp")
        result.update(
            {
                "nation": f"{kwargs['nation']}.public.{kwargs['nation'][:-1]}_{scale}_nation"
            }
        ) if "nation" in kwargs else missing_tables.append("nation")
        result.update(
            {
                "region": f"{kwargs['region']}.public.{kwargs['region'][:-1]}_{scale}_region"
            }
        ) if "region" in kwargs else missing_tables.append("region")
        return result
