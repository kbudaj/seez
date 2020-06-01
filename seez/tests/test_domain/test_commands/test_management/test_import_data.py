import pytest
from assertpy.assertpy import assert_that

from seez.domain.models import Car
from seez.management.commands.import_data import Command


@pytest.mark.postgres_db
class TestImportDataCommand:
    def test_import(
        self, make_repository, model_repository, car_repository, submodel_repository
    ):
        assert_that(make_repository.get_all()).is_length(0)
        assert_that(model_repository.get_all()).is_length(0)
        assert_that(submodel_repository.get_all()).is_length(0)
        assert_that(car_repository.get_all()).is_length(0)

        cmd = Command()
        cmd.path = "/app/seez/tests/files/"
        cmd.handle()

        makes = make_repository.get_all()
        make_names = {make.name for make in makes}
        assert_that(make_names).is_equal_to({"Honda", "Nissan"})

        models = model_repository.get_all()
        model_names = {model.name for model in models}
        assert_that(model_names).is_equal_to({"Accord", "Tiida"})

        submodels = submodel_repository.get_all()
        submodel_names = {submodel.name for submodel in submodels}
        assert_that(submodel_names).is_equal_to({"some honda", "some nissan"})

        cars = car_repository.get_all()
        nissan, honda = None, None
        if cars[0].make_name == "Nissan":
            nissan, honda = cars[0], cars[1]
        else:
            honda, nissan = cars[1], cars[0]

        assert_that(nissan.active).is_true()
        assert_that(nissan.year).is_equal_to(2016)
        assert_that(nissan.mileage).is_equal_to(54089)
        assert_that(nissan.price).is_equal_to(35902)
        assert_that(nissan.make_name).is_equal_to("Nissan")
        assert_that(nissan.model_name).is_equal_to("Tiida")
        assert_that(nissan.submodel_name).is_equal_to("some nissan")
        assert_that(nissan.body_type).is_equal_to(Car.BodyType.HATCHBACK)
        assert_that(nissan.transmission).is_equal_to(Car.Transmission.AUTOMATIC)
        assert_that(nissan.fuel_type).is_equal_to(Car.FuelType.PETROL)
        assert_that(nissan.exterior_color).is_equal_to("White")

        assert_that(honda.active).is_false()
        assert_that(honda.year).is_equal_to(2015)
        assert_that(honda.mileage).is_equal_to(76000)
        assert_that(honda.price).is_equal_to(55000)
        assert_that(honda.make_name).is_equal_to("Honda")
        assert_that(honda.model_name).is_equal_to("Accord")
        assert_that(honda.submodel_name).is_equal_to("some honda")
        assert_that(honda.body_type).is_equal_to(Car.BodyType.SEDAN)
        assert_that(honda.transmission).is_equal_to(Car.Transmission.MANUAL)
        assert_that(honda.fuel_type).is_none()
        assert_that(honda.exterior_color).is_equal_to("White")
