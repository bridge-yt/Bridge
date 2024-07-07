package bridge

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/hashicorp/terraform-plugin-sdk/v2/diag"
	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"
)

func dataSourceBridgeValue() *schema.Resource {
	return &schema.Resource{
		ReadContext: dataSourceBridgeValueRead,
		Schema: map[string]*schema.Schema{
			"name": {
				Type:     schema.TypeString,
				Required: true,
			},
			"value": {
				Type:     schema.TypeString,
				Computed: true,
			},
			"arn": {
				Type:     schema.TypeString,
				Computed: true,
			},
			"resource_type": {
				Type:     schema.TypeString,
				Computed: true,
			},
		},
	}
}

func dataSourceBridgeValueRead(ctx context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	apiURL := meta.(map[string]interface{})["api_url"].(string)
	name := d.Get("name").(string)

	url := fmt.Sprintf("%s/resource/%s", apiURL, name)
	resp, err := http.Get(url)
	if err != nil {
		return diag.FromErr(err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return diag.Errorf("Error fetching resource: %s", resp.Status)
	}

	var result OutputResource
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return diag.FromErr(err)
	}

	if err := d.Set("value", result.Value); err != nil {
		return diag.FromErr(err)
	}

	if err := d.Set("arn", result.Arn); err != nil {
		return diag.FromErr(err)
	}

	if err := d.Set("resource_type", result.ResourceType); err != nil {
		return diag.FromErr(err)
	}

	d.SetId(name)
	return nil
}
