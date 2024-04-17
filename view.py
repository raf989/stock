"""tewtw."""

from models import Order, OrderProductLink, Product, Rack, RackProductLink


class View:
    """dfdfsg."""

    def __init__(self: "View", order_numbers: list[int]) -> None:
        """_summary_.

        Args:
        ----
            self (View): _description_.
            order_numbers (list[int]): _description_.

        """
        n = "\n"
        self.order_numbers = order_numbers
        self.racks = self._get_racks()
        self.racks = [
            n.join(
                [
                    f"===Стеллаж {rack}\n"
                    + n.join(
                        [
                            f"{product.name} (art={product.article})\n"
                            f"заказ {number}, {count} шт.\n"
                            + (
                                f"доп стеллаж: {', '.join(an_racks)}\n"
                                if an_racks
                                else ""
                            )
                            for _, product, number, count, an_racks in products
                        ],
                    )
                    for rack, products in self.racks.items()
                ],
            ),
        ]
        self.rackviews = "".join(self.racks)

    def _get_racks(self: "View") -> dict:
        """_summary_.

        Args:
        ----
            self (View): _description_.

        """
        order_product: dict[int, list[Product]] = {
            number: [
                (Product.get_by("id", link.product_id), link.count)
                # собираем список кортежей c продуктами
                # и их количеством для заказа
                for link in OrderProductLink.get_all_by(
                    "order_id",
                    Order.get_by("order_number", number).id,
                )  # получаем обьект линка по внутреннему id заказа
            ]
            for number in self.order_numbers
        }
        # {10: [(Ноутбук, 2), (Телефон, 1) ...]}
        racks = [
            (
                Rack.get_by("id", link.rack_id).name,
                product,
                number,
                count,
                [
                    Rack.get_by("id", link.rack_id).name
                    for link in RackProductLink.get_all_by(
                        "product_id",
                        product.id,
                    )
                    if not link.main
                ],
            )
            for number, products in order_product.items()
            # (10, [(Ноутбук, 2), ....])
            for product, count in products  # (Ноутбук, 2)
            for link in RackProductLink.get_all_by("product_id", product.id)
            # Ноутбук может лежать на стеллаже
            # А, c доп стеллажами З В  # noqa: RUF003
            if link.main
        ]
        result = {}
        for rack, product, number, count, an_racks in racks:
            if rack in result:  # группируем по стелажу
                result[rack].append(
                    (rack, product, number, count, an_racks),
                )
            else:
                result[rack] = [
                    (rack, product, number, count, an_racks),
                ]
        for products in result.values():
            products.sort(key=lambda x: x[2])
        return result

    def __str__(self: "View") -> str:
        """dfhdfh.

        Args:
        ----
            self (View): _description_.

        Returns:
        -------
            _type_: _description_.

        """
        return (
            f"=+=+=+=\n"
            f"Страница сборки заказов "
            f"{', '.join(map(str,self.order_numbers))}\n\n"
            f"{self.rackviews}"
        )
