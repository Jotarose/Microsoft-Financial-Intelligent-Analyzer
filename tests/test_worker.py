from types import SimpleNamespace

from src.client import Report
from src.worker import extract_financial_data


class FakeClient:
    def __init__(self, html: str):
        self._html = html

    def get_url_content(self, url: str):
        return SimpleNamespace(text=self._html)


def test_no_income_table_returns_error():
    html = "<html><body><div>NOT THE TABLE</div><p>Some content</p></body></html>"
    client = FakeClient(html)
    report = Report(year=2023, url="http://example.com/no-table")
    result = extract_financial_data(client, report)

    assert isinstance(result, dict)
    assert result["year"] == 2023
    assert result.get("error") == "Tabla no encontrada"


def test_extract_financial_data_parses_table():
    html = """
    <html>
      <body>
        <div>INCOME STATEMENTS</div>
        <table>
          <tr>
            <td>Revenue</td>
            <td>1000</td>
          </tr>
          <tr>
            <td class="cell-indent">Product</td>
            <td>800</td>
          </tr>
          <tr>
            <td class="cell-indent-double">Services</td>
            <td>200</td>
          </tr>
          <tr>
            <td>Operating income</td>
            <td>50</td>
          </tr>
          <!-- row with empty title should be ignored -->
          <tr>
            <td class="cell-indent"></td>
            <td>0</td>
          </tr>
          <!-- row with empty value should be ignored -->
          <tr>
            <td class="cell-indent">Deferred</td>
            <td></td>
          </tr>
        </table>
      </body>
    </html>
    """
    client = FakeClient(html)
    report = Report(year=2024, url="http://example.com/report")
    result = extract_financial_data(client, report)

    expected = {
        "year": 2024,
        "data": {
            "Revenue": {
                "Total": "1000",
                "Product": "800",
                "Services": "200",
            },
            "Operating income": {"Total": "50"},
        },
    }

    assert result == expected
