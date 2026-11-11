import sqlite3
import tempfile
import unittest
import zipfile
from contextlib import closing
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from project import pipeline


class FakeResponse:
    def __init__(self, content: bytes):
        self.content = content

    def raise_for_status(self):
        return None


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.source = pd.DataFrame(
            {
                "Country Name": ["Canada", "Canada", "United States"],
                "Country Code": ["CAN", "CAN", "USA"],
                "Indicator Name": ["Renewable energy", "Renewable energy", "Renewable energy"],
                "2015": [10.0, None, 12.0],
                "2016": [11.0, 12.0, 13.0],
            }
        )

    def test_clean_and_reshape_filters_countries_and_null_values(self):
        cleaned = pipeline.clean_and_reshape_data(
            self.source,
            countries=["Canada"],
            years=["2015", "2016"],
        )

        self.assertEqual(cleaned["Country Name"].unique().tolist(), ["Canada"])
        self.assertEqual(cleaned["Year"].tolist(), ["2015", "2016", "2016"])
        self.assertEqual(cleaned["Value"].tolist(), [10.0, 11.0, 12.0])

    def test_clean_and_reshape_reports_missing_columns(self):
        with self.assertRaisesRegex(ValueError, "missing required columns"):
            pipeline.clean_and_reshape_data(
                self.source.drop(columns=["2015"]),
                countries=["Canada"],
                years=["2015", "2016"],
            )

    @patch("project.pipeline.requests.get")
    def test_download_indicator_csv_reads_data_from_archive(self, mock_get):
        archive_bytes = BytesIO()
        with zipfile.ZipFile(archive_bytes, "w") as archive:
            archive.writestr(
                "API_TEST_DS2_en_csv_v1.csv",
                "metadata row 1\nmetadata row 2\nmetadata row 3\nmetadata row 4\n"
                "Country Name,Country Code,Indicator Name,2015\nCanada,CAN,Test,10\n",
            )
        mock_get.return_value = FakeResponse(archive_bytes.getvalue())

        result = pipeline.download_indicator_csv("TEST")

        self.assertEqual(result.loc[0, "Country Name"], "Canada")
        self.assertEqual(mock_get.call_args.kwargs["timeout"], 60)

    def test_save_outputs_writes_csv_and_sqlite_table(self):
        data = pipeline.clean_and_reshape_data(
            self.source,
            countries=["Canada"],
            years=["2015", "2016"],
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_dir = Path(temporary_directory)
            database_path = output_dir / "data.db"
            with patch.object(pipeline, "DATA_DIR", output_dir):
                pipeline.save_outputs(data, "test_indicator", database_path)

            csv_data = pd.read_csv(output_dir / "test_indicator_cleaned.csv")
            self.assertEqual(len(csv_data), len(data))
            with closing(sqlite3.connect(database_path)) as connection:
                count = connection.execute(
                    "SELECT COUNT(*) FROM test_indicator_data"
                ).fetchone()[0]
            self.assertEqual(count, len(data))

    def test_save_outputs_rejects_empty_data(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            with self.assertRaisesRegex(ValueError, "No observations found"):
                pipeline.save_outputs(
                    pd.DataFrame(),
                    "test_indicator",
                    Path(temporary_directory) / "data.db",
                )


if __name__ == "__main__":
    unittest.main()
